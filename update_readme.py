"""
update_readme.py

Auto-generates the "Projects" table and "Requirements" section of the
parent README.md by scanning subfolders in the repository.

Usage:
    python update_readme.py

Run this from the ROOT of your repository (same folder as the parent README.md).
"""

import os
import re
import ast

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(ROOT_DIR, "README.md")

# Folders to ignore when scanning for projects
IGNORE_DIRS = {".git", "__pycache__", "venv", "env", ".venv", "node_modules", "scripts"}

# Standard library modules to exclude when detecting "key libraries"
import sys
STDLIB_MODULES = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else set()


def get_project_folders():
    """Return a list of top-level subfolders that look like projects (contain .py files)."""
    folders = []
    for entry in sorted(os.listdir(ROOT_DIR)):
        full_path = os.path.join(ROOT_DIR, entry)
        if not os.path.isdir(full_path) or entry in IGNORE_DIRS or entry.startswith("."):
            continue
        has_py = any(f.endswith(".py") for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f)))
        # also check one level deeper (e.g. Django apps nested inside project folder)
        if not has_py:
            for sub in os.listdir(full_path):
                sub_path = os.path.join(full_path, sub)
                if os.path.isdir(sub_path) and any(f.endswith(".py") for f in os.listdir(sub_path) if os.path.isfile(os.path.join(sub_path, f))):
                    has_py = True
                    break
        if has_py:
            folders.append(entry)
    return folders


def get_description(folder):
    """Pull a short description from the project's own README.md, if present."""
    readme_path = os.path.join(ROOT_DIR, folder, "README.md")
    if not os.path.isfile(readme_path):
        return "_No description available (add a README.md inside this folder)_"
    with open(readme_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    title = folder.replace("_", " ").title()
    description = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not title_found(title):
            title = strip_emoji(stripped.lstrip("#").strip())
        elif stripped and not stripped.startswith("#") and not stripped.startswith("!") and description is None:
            description = stripped
        if title and description:
            break

    if description is None:
        description = "_No description available_"

    return title, description


def title_found(_):
    return False  # placeholder helper kept simple; title always taken from first heading


def strip_emoji(text):
    return re.sub(r"[^\w\s\-.,()]", "", text).strip()


def get_libraries(folder):
    """Detect imported third-party libraries by parsing all .py files in the folder (recursively)."""
    libs = set()
    folder_path = os.path.join(ROOT_DIR, folder)

    for dirpath, _, filenames in os.walk(folder_path):
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=fpath)
            except (SyntaxError, UnicodeDecodeError):
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        libs.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        libs.add(node.module.split(".")[0])

    # Remove standard library and local/project-relative modules
    third_party = sorted(
        lib for lib in libs
        if lib not in STDLIB_MODULES
        and not lib.startswith("_")
        and lib not in ("django",)  # handled separately below if you want django excluded/included
    )

    # keep django explicitly if used, since it's central to these projects
    if "django" in libs:
        third_party = ["django"] + third_party

    return third_party


def build_projects_table(folders):
    rows = ["| Project | Description | Key Libraries |", "|---|---|---|"]
    all_libs = set()

    for folder in folders:
        title, description = get_description(folder)
        libs = get_libraries(folder)
        all_libs.update(libs)
        libs_str = ", ".join(f"`{lib}`" for lib in libs) if libs else "-"
        rows.append(f"| [📁 {title}](./{folder}/README.md) | {description} | {libs_str} |")

    return "\n".join(rows), sorted(all_libs)


def build_requirements_block(all_libs):
    lines = ["- Python 3.8+", "", "**Install via pip:**"]
    for lib in all_libs:
        lines.append(f"- [`{lib}`](https://pypi.org/project/{lib}/)")
    lines.append("")
    lines.append("Install all at once:")
    lines.append("```bash")
    lines.append(f"pip install {' '.join(all_libs)}" if all_libs else "pip install -r requirements.txt")
    lines.append("```")
    return "\n".join(lines)


def replace_between_markers(content, start_marker, end_marker, new_block):
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    replacement = f"{start_marker}\n{new_block}\n{end_marker}"
    return pattern.sub(replacement, content)


def main():
    if not os.path.isfile(README_PATH):
        print(f"README.md not found at {README_PATH}. Run this script from the repo root.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    folders = get_project_folders()
    if not folders:
        print("No project folders with .py files found.")
        return

    projects_table, all_libs = build_projects_table(folders)
    requirements_block = build_requirements_block(all_libs)

    content = replace_between_markers(content, "<!-- PROJECTS_START -->", "<!-- PROJECTS_END -->", projects_table)
    content = replace_between_markers(content, "<!-- REQUIREMENTS_START -->", "<!-- REQUIREMENTS_END -->", requirements_block)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"README.md updated with {len(folders)} project(s) and {len(all_libs)} librar(y/ies).")


if __name__ == "__main__":
    main()
