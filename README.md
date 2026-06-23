# Secure API

A REST API built with Python and FastAPI, focused on security best practices.

## Tech Stack

- **Python 3.11**
- **FastAPI** — modern, fast web framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM for database interaction
- **JWT** — stateless authentication with python-jose
- **bcrypt** — password hashing via passlib
- **slowapi** — rate limiting

- Refresh token with 7-day expiration
- JWT blacklist on logout (token revocation)
- CORS configured for frontend origins
- Token type validation (access vs refresh)

## Project Structure

secure-api/

├── app/

│   ├── main.py          # Application entry point

│   ├── database.py      # Database connection and session

│   ├── models/

│   │   └── user.py      # User database model

│   ├── routers/

│   │   └── auth.py      # Authentication endpoints

│   ├── services/

│   │   └── user_service.py  # Business logic

│   └── utils/

│       └── security.py  # JWT and password utilities

├── .env                 # Environment variables (not committed)

├── requirements.txt

└── README.md


## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | No | Health check |
| GET | `/health` | No | Server status |
| POST | `/auth/register` | No | Register new user |
| POST | `/auth/login` | No | Login and get JWT tokens |
| GET | `/auth/me` | Yes | Get current user info |
| POST | `/auth/refresh` | No | Get new access token |
| POST | `/auth/logout` | Yes | Invalidate current token |
| GET | `/auth/suspicious-access` | Yes | Check token and user status |
| GET | `/tasks/` | Yes | List all user tasks |
| POST | `/tasks/` | Yes | Create a new task |
| GET | `/tasks/{task_id}` | Yes | Get a specific task |
| PUT | `/tasks/{task_id}` | Yes | Update a task |
| DELETE | `/tasks/{task_id}` | Yes | Delete a task |

## Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/secure-api.git
cd secure-api

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run the server
uvicorn app.main:app --reload
```

## Environment Variables

DATABASE_URL=postgresql://postgres:password@localhost:5432/secureapi

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

## API Documentation

Interactive documentation available at `http://localhost:8000/docs`