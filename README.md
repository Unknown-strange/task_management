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
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/taskdb
DATABASE_URL_SYNC=postgresql://postgres:postgres@db:5432/taskdb
SECRET_KEY=your-secret-key-here-change-this-in-production-min-32-chars
ALGORITHM=HS256
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

### User Endpoints

*(To be implemented)*
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - Login user
- `POST /api/v1/users/refresh` - Refresh access token
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile

### Task Endpoints

*(To be implemented)*
- `GET /api/v1/tasks` - List all tasks
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{task_id}` - Get task by ID
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task

## Database Models

### User Model

- `id`: UUID (Primary Key)
- `email`: String (Unique)
- `username`: String (Unique)
- `hashed_password`: String
- `full_name`: String (Optional)
- `is_active`: Boolean
- `is_superuser`: Boolean
- `is_verified`: Boolean
- `created_at`: DateTime
- `updated_at`: DateTime

### Task Model

- `id`: UUID (Primary Key)
- `title`: String
- `description`: Text (Optional)
- `priority`: Enum (LOW, MEDIUM, HIGH)
- `status`: Enum (TODO, IN_PROGRESS, DONE)
- `is_completed`: Boolean
- `user_id`: UUID (Foreign Key)
- `due_date`: DateTime (Optional)
- `category`: String (Optional)
- `created_at`: DateTime
- `updated_at`: DateTime

## Development

### Running Locally (Without Docker)

1. Create a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`

4. Start PostgreSQL (ensure it's running on localhost:5432)

5. Run migrations:

```bash
alembic upgrade head
```

6. Start the application:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild containers
docker compose up -d --build

# Access API container shell
docker compose exec api bash

# Access database
docker compose exec db psql -U postgres -d taskdb
```

### Database Migrations

```bash
# Create new migration
docker compose exec api alembic revision --autogenerate -m "Description"

# Apply migrations
docker compose exec api alembic upgrade head

# Rollback migration
docker compose exec api alembic downgrade -1

# View migration history
docker compose exec api alembic history
```

## Configuration

Configuration is managed through environment variables defined in `.env` and loaded via `app/core/config.py`.

Key settings:
- `APP_NAME`: Application name
- `API_V1_PREFIX`: API version prefix (default: /api/v1)
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: Async database connection string
- `DATABASE_URL_SYNC`: Sync database connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration

## Testing

*(To be implemented)*

```bash
# Run tests
docker compose exec api pytest

# Run tests with coverage
docker compose exec api pytest --cov=app tests/
```

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- CORS is configured (currently allows all origins - update for production)
- Rate limiting enabled
- Environment variables for sensitive data

**Production Security Checklist**:
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Update CORS settings to allow only specific origins
- [ ] Use HTTPS in production
- [ ] Enable database connection encryption
- [ ] Configure rate limiting thresholds
- [ ] Set up monitoring and logging

## Troubleshooting

### API Container Not Running

Check logs:
```bash
docker compose logs api
```

Common issues:
- Import errors: Check Python syntax in model files
- Database connection: Ensure PostgreSQL is healthy
- Port conflicts: Ensure port 8000 is available

### Database Connection Issues

```bash
# Check database status
docker compose ps

# Restart database
docker compose restart db
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue in the repository.
