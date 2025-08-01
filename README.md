# 📈 Django Company Watchlist API

A Django REST Framework project that provides user authentication and endpoints to manage companies and a user's watchlist.

---

## 🚀 Features

- User Registration & Login (JWT Auth)
- Optional Google OAuth
- Watchlist APIs
- Company search, filter, and pagination
- Token-secured endpoints
- Dockerized for easy deployment
- Request & response logging middleware

---

## 🛠 Tech Stack

- Django + Django REST Framework
- PostgreSQL / SQLite
- JWT Authentication
- Docker

---

## 🐳 Setup with Docker

```bash
# Build and start the container
docker build -t tradeapp .
docker run -p 8000:8000 tradeapp
