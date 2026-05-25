ERP Backend API v2

A production-ready ERP backend API built with Django REST Framework, PostgreSQL, Docker, and JWT authentication.

This project provides a scalable multi-tenant ERP backend system for managing organizations, customers, products, and orders through a secure REST API.

⸻

Live API Documentation

Swagger UI

https://erp-backend-django-v2.onrender.com/api/docs/

ReDoc

https://erp-backend-django-v2.onrender.com/api/redoc/

⸻

Features

* JWT Authentication
* Multi-tenant Organization System
* Product Management
* Customer Management
* Order Management
* Order Items
* Role-based Permissions
* Search, Filtering, and Ordering
* Service Layer Architecture
* PostgreSQL Database
* Dockerized Deployment
* Swagger / ReDoc API Documentation
* Automated Testing with Pytest
* 92% Test Coverage
* Production Deployment on Render

⸻

Tech Stack

Backend

* Python 3.12
* Django 5
* Django REST Framework

Database

* PostgreSQL

Authentication

* Simple JWT

DevOps

* Docker
* Docker Compose
* Gunicorn
* WhiteNoise
* Render

Testing

* Pytest
* Pytest-Django
* Coverage

⸻

Project Structure

accounts/
customers/
orders/
products/
erp_v2/

The project follows a service-layer architecture to separate business logic from views and serializers.

⸻

API Modules

Accounts

* User Registration
* JWT Login / Refresh
* Organization-based Access Control

Customers

* Create / Update / Delete Customers
* Organization Isolation
* Search & Filtering

Products

* Product CRUD Operations
* Stock Management
* Filtering / Ordering / Search

Orders

* Create Orders
* Order Status Management
* Stock Validation
* Atomic Transactions
* Order Items Management

⸻

Authentication

The API uses JWT Authentication.

Obtain Token

POST /api/token/

Refresh Token

POST /api/token/refresh/

⸻

Running Locally

Clone the repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

Navigate into the project

cd ERP_backend-django--v2

Create virtual environment

python -m venv venv

Activate virtual environment

macOS / Linux

source venv/bin/activate

Windows

venv\Scripts\activate

⸻

Install Dependencies

pip install -r requirements.txt

⸻

Environment Variables

Create a .env file:

DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
ALLOWED_HOSTS=127.0.0.1,localhost

⸻

Run Migrations

python manage.py migrate

⸻

Run Development Server

python manage.py runserver

⸻

Docker Setup

Build and Run

docker compose up --build

⸻

Run Tests

pytest

⸻

Run Coverage

pytest --cov=. --cov-report=term-missing

Current coverage:

92%

⸻

Production Features

* PostgreSQL Production Database
* Dockerized Deployment
* WhiteNoise Static Files
* Gunicorn WSGI Server
* Environment-based Settings
* Secure JWT Authentication

⸻

API Documentation

Interactive API documentation is available through Swagger and ReDoc.

Swagger

https://erp-backend-django-v2.onrender.com/api/docs/

ReDoc

https://erp-backend-django-v2.onrender.com/api/redoc/

⸻

Deployment

The project is deployed on Render using:

* Docker
* PostgreSQL
* Gunicorn
* WhiteNoise

⸻

Future Improvements

* Redis Caching
* Celery Background Tasks
* Email Notifications
* File Uploads
* WebSockets
* CI/CD Pipelines
* AWS Deployment
* Rate Limiting Enhancements

⸻

Author

Built by Soufyane BLG