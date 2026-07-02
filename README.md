# 🐍 Django Mini Projects
A collection of mini projects built using **Python and Django** — a high-level web framework that enables rapid development of secure and maintainable websites. Each project is self-contained in its own folder with its own code and documentation.

---

## 📋 Table of Contents
- [About Django](#about-django)
- [Projects](#projects)
- [Requirements](#requirements)
- [How to Run Any Project](#how-to-run-any-project)
- [Repository Structure](#repository-structure)
- [Author](#author)

---

## 🐍 About Django
`Django` is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It comes with a built-in admin panel, ORM, authentication system, and URL routing — making it ideal for building anything from simple websites to full-scale web applications.


---

<!-- PROJECTS_START -->
## 🗂️ Projects
| Project | Description | Key Libraries |
|---|---|---|
| [📁 django_usingviews](./django_usingviews/README.md) | _it is a basic django project using only the views of the app to show the text on the hostserver produced by the django framework_ | `django` |


<!-- PROJECTS_END -->

---

<!-- REQUIREMENTS_START -->
## 🛠️ Requirements
- Python 3.8+
- [Anaconda](https://www.anaconda.com/download) (optional, used for environment management)

**Install via pip:**
- [`django`](https://pypi.org/project/Django/) — high-level Python web framework

Install all at once:
```bash
pip install django
```
<!-- REQUIREMENTS_END -->

---
## Create a django project

1. Create a django project
   ```bash
   django-admin startproject projectname
   ```
2. Navigate into the project folder:
   ```bash
   cd projectname
   ```
3. create a app
   ```bash
   django-admin startapp appname
   ```
## 🚀 How to Run Any Project

1. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Run the development server:
   ```bash
   python manage.py runserver
   ```
3. Visit `http://127.0.0.1:8000/` in your browser.

---


---

## 👤 Author
- **Your Name** — [DadiRohit45](https://github.com/DadiRohit45)

---

## 📄 License
This repository is open-source and available under the [MIT License](LICENSE).
