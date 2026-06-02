# Task Management API

A modern, scalable REST API for task management built with FastAPI, PostgreSQL, and Docker.

## Features

- **User Management**: User registration, authentication, and profile management
- **Task Management**: Create, read, update, and delete tasks with priorities and statuses
- **Authentication**: JWT-based authentication with access and refresh tokens
- **Database**: PostgreSQL with SQLAlchemy 2.0 ORM and async support
- **Migrations**: Alembic for database schema versioning
- **Rate Limiting**: API rate limiting with SlowAPI
- **CORS**: Configurable CORS for frontend integration
- **Docker**: Fully containerized with Docker Compose
- **API Documentation**: Auto-generated with OpenAPI (Swagger)

## Tech Stack

- **Framework**: FastAPI 0.136.3
- **Database**: PostgreSQL 16 (Alpine)
- **ORM**: SQLAlchemy 2.0.50 with asyncpg
- **Migrations**: Alembic 1.18.4
- **Authentication**: JWT (python-jose), bcrypt, passlib
- **Validation**: Pydantic 2.13.4
- **Server**: Uvicorn 0.48.0
- **Containerization**: Docker & Docker Compose

## Project Structure

```
task-api/
├── app/
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   └── database.py        # Database connection setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   └── task.py            # Task model
│   └── main.py                # Application entry point
├── alembic/                   # Database migrations
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker services configuration
└── README.md                  # This file
```

## Prerequisites

- Docker Desktop installed
- Docker Compose installed
- (Optional) Python 3.12+ for local development

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd task-api
```

### 2. Environment Configuration

Create a `.env` file in the root directory (or use the existing one):

```env
DATABASE_URL=XXXXXXXXX
DATABASE_URL_SYNC=XXXXXXXXXXX
SECRET_KEY=XXXXXX
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Important**: Change the `SECRET_KEY` in production to a strong, random string (minimum 32 characters).

### 3. Start the Application

```bash
docker compose up -d --build
```

This will:
- Build the API Docker image
- Start PostgreSQL database
- Start the FastAPI application on port 8000

### 4. Initialize Database

Run database migrations:

```bash
docker compose exec api alembic revision --autogenerate -m "Create users and tasks tables"
docker compose exec api alembic upgrade head
```

### 5. Access the API

- **API Base URL**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/api/v1/docs
- **API Documentation (ReDoc)**: http://localhost:8000/api/v1/redoc

## API Endpoints

### Health Check

- `GET /` - Root endpoint
- `GET /api/v1/health` - Health check endpoint

