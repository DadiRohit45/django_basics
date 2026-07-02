# 📝 Django Using Views

A basic Django project demonstrating how **views** work within a Django app — routing a URL to a view function that returns a response. Built using the `django_text` app inside the `django_usingviews` project.

---

## 📋 Table of Contents
- [About This Project](#about-this-project)
- [Project Structure](#project-structure)
- [How Routing Works Here](#how-routing-works-here)
- [Requirements](#requirements)
- [Setup & Run](#setup--run)
- [Testing](#testing)
- [Author](#author)

---

## 📖 About This Project
This project demonstrates the fundamentals of **Django views** — the Python functions (or classes) that take a web request and return a web response. It shows how a project's URL configuration delegates routing to an app's own `urls.py`, which in turn maps a path to a view function.

**Project name:** `django_usingviews`
**App name:** `django_text`

---

## 🗂️ Project Structure
```text
django_usingviews/
│
├── manage.py
│
├── django_usingviews/              ← project-level config
│   ├── settings.py                 ← project settings, registered apps
│   ├── urls.py                     ← root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
└── django_text/                    ← app-level code
    ├── urls.py                     ← app URL configuration
    ├── views.py                    ← view logic (e.g. `show`)
    ├── models.py
    ├── tests.py
    └── ...
```

---

## 🔗 How Routing Works Here

### 1. Project-level `urls.py`
The root URL configuration includes the app's URLs under the `django_text/` path:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("django_text/", include("django_text.urls")),
]
```

### 2. App-level `urls.py`
Inside the `django_text` app, the root of that included path (`django_text/`) is mapped to a view called `show`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show, name="textshowed"),
]
```

### 3. Result
Visiting:
```
http://127.0.0.1:8000/django_text/
```
triggers the `show` view function defined in `django_text/views.py`, which returns the response (e.g. rendered text or a template).

---

## ✅ Requirements
- Python 3.8+
- Django 6.0.6

Install via pip:
```bash
pip install django
```

---

## 🚀 Setup & Run

1. Clone the repository and navigate into the project folder:
   ```bash
   cd django_usingviews
   ```
2. Install dependencies:
   ```bash
   pip install django
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. Visit the app route in your browser:
   ```
   http://127.0.0.1:8000/django_text/
   ```



---

## ⚙️ Key Settings (`settings.py`)
- **Installed apps:** `django_text` added to `INSTALLED_APPS`
- **Root URL config:** `django_usingviews.urls`
- **Database:** SQLite (`db.sqlite3`)
- **Debug mode:** `True` (development only — set to `False` in production)

> ⚠️ Note: This project currently uses Django's default `SECRET_KEY` and has `DEBUG = True`. Before deploying to production, move the secret key to an environment variable and set `DEBUG = False`.

---

## 👤 Author
- **Your Name** — [DadiRohit45](https://github.com/DadiRohit45)

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
