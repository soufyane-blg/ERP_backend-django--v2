# ERP Backend API v2

A production-ready ERP backend API built with Django REST Framework, PostgreSQL, Docker, and JWT authentication.

This project provides a scalable multi-tenant ERP backend system for managing organizations, customers, products, and orders through a secure REST API.

---

# Live API Documentation

## Swagger UI

https://erp-backend-django-v2.onrender.com/api/docs/

## ReDoc

https://erp-backend-django-v2.onrender.com/api/redoc/

---

# Features

- JWT Authentication
- Multi-tenant Organization System
- Product Management
- Customer Management
- Order Management
- Order Items Management
- Role-based Permissions
- Search, Filtering, and Ordering
- Service Layer Architecture
- PostgreSQL Database
- Dockerized Deployment
- Swagger / ReDoc API Documentation
- Automated Testing with Pytest
- 92% Test Coverage
- Production Deployment on Render

---

# Tech Stack

## Backend

- Python 3.12
- Django 5
- Django REST Framework

## Database

- PostgreSQL

## Authentication

- Simple JWT

## DevOps & Deployment

- Docker
- Docker Compose
- Gunicorn
- WhiteNoise
- Render

## Testing

- Pytest
- Pytest-Django
- Coverage.py

---

# Project Structure

```bash
accounts/
customers/
orders/
products/
erp_v2/
```

The project follows a service-layer architecture to separate business logic from views and serializers, making the codebase cleaner, scalable, and easier to maintain.

---

# API Modules

## Accounts

- User Registration
- JWT Login / Token Refresh
- Organization-based Access Control

## Customers

- Create / Update / Delete Customers
- Organization Isolation
- Search & Filtering

## Products

- Product CRUD Operations
- Stock Management
- Filtering / Ordering / Search

## Orders

- Create Orders
- Order Status Management
- Stock Validation
- Atomic Transactions
- Order Items Management

---

# Authentication

The API uses JWT Authentication.

## Obtain Access & Refresh Tokens

```http
POST /api/token/
```

## Refresh Access Token

```http
POST /api/token/refresh/
```

---

# Running Locally

## Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

## Navigate into the Project

```bash
cd ERP_backend-django--v2
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True

SECRET_KEY=your_secret_key

DATABASE_URL=your_database_url

ALLOWED_HOSTS=127.0.0.1,localhost
```

---

# Apply Migrations

```bash
python manage.py migrate
```

---

# Run Development Server

```bash
python manage.py runserver
```

---

# Docker Setup

## Build and Run Containers

```bash
docker compose up --build
```

---

# Run Tests

```bash
pytest
```

---

# Run Coverage Report

```bash
pytest --cov=. --cov-report=term-missing
```

Current coverage:

```text
92%
```

---

# Production Features

- PostgreSQL Production Database
- Dockerized Deployment
- WhiteNoise Static Files Handling
- Gunicorn WSGI Server
- Environment-based Settings
- Secure JWT Authentication

---

# API Documentation

Interactive API documentation is available through Swagger UI and ReDoc.

## Swagger UI

https://erp-backend-django-v2.onrender.com/api/docs/

## ReDoc

https://erp-backend-django-v2.onrender.com/api/redoc/

---

# Deployment

The project is deployed on Render using:

- Docker
- PostgreSQL
- Gunicorn
- WhiteNoise

---

# Future Improvements

- Redis Caching
- Celery Background Tasks
- Email Notifications
- File Uploads
- WebSockets
- CI/CD Pipelines
- AWS Deployment
- Advanced Rate Limiting

---

# Author

Built by Soufyane BLG.