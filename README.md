# puck-booking

Hyperspecific hockey game booking API built with FastAPI.

## Overview

This is a FastAPI-based backend API for booking hockey matches at DNB Arena. The system:
- Syncs match data from an external hockey API
- Only includes matches at DNB Arena with "Scheduled" status
- Allows users to register and book matches
- Enforces a maximum of 2 bookings per match
- Provides admin capabilities for managing users and bookings

## Features

- **User Authentication**: Register, login, and JWT-based authentication
- **Match Management**: View available matches and sync from external API
- **Booking System**: Book matches with automatic validation (max 2 per match)
- **Admin Functions**: Manage users and bookings
- **Auto-generated API Documentation**: Available at `/docs` (Swagger UI)
- **Docker Support**: Easy deployment with Docker and docker-compose

## Tech Stack

- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: SQL ORM for database operations
- **SQLite**: Database (easily switchable to PostgreSQL/MySQL)
- **JWT**: Token-based authentication
- **Pydantic**: Data validation using Python type annotations
- **httpx**: Async HTTP client for external API calls
- **Docker**: Containerization for easy deployment

## Installation

### Option 1: Docker (Recommended for Production)

1. Clone the repository:
```bash
git clone https://github.com/MathiasDevelopes/puck-booking.git
cd puck-booking
```

2. Create a `.env` file for configuration:
```env
SECRET_KEY=your-super-secret-key-change-this-in-production
CORS_ORIGINS=*
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. Run with docker-compose:
```bash
docker-compose up -d
```

The API will be available at http://localhost:8000

### Option 2: Local Development

#### Prerequisites

- Python 3.8 or higher
- pip

#### Setup

1. Clone the repository:
```bash
git clone https://github.com/MathiasDevelopes/puck-booking.git
cd puck-booking
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Create a `.env` file for configuration:
```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./hockey_booking.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

### Development Server
```bash
uvicorn app.main:app --reload
```

### Production with Docker
```bash
docker-compose up -d
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Users

- `POST /api/v1/users/register` - Register a new user
- `POST /api/v1/users/login` - Login and get JWT token
- `GET /api/v1/users/me` - Get current user info (requires auth)
- `DELETE /api/v1/users/{user_id}` - Delete a user (admin only)

### Matches

- `GET /api/v1/matches/` - List all upcoming matches
- `GET /api/v1/matches/{match_id}` - Get specific match details
- `POST /api/v1/matches/sync` - Sync matches from external API (admin only)

### Bookings

- `POST /api/v1/bookings/` - Create a new booking
- `GET /api/v1/bookings/my-bookings` - Get current user's bookings
- `GET /api/v1/bookings/match/{match_id}` - Get bookings for a specific match
- `DELETE /api/v1/bookings/{booking_id}` - Delete a booking
- `GET /api/v1/bookings/` - List all bookings (admin only)

## Usage Examples

### Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepassword"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### List Matches

```bash
curl -X GET "http://localhost:8000/api/v1/matches/"
```

Response:
```json
[
  {
    "external_id": 8183228,
    "date": "2026-02-09T17:00:00Z",
    "name": "Oilers vs Lørenskog",
    "arena": "DNB Arena",
    "id": 1,
    "bookings_count": 0,
    "is_full": false
  }
]
```

### Create a Booking

```bash
curl -X POST "http://localhost:8000/api/v1/bookings/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"match_id": 1}'
```

### Delete a User (Admin)

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/1" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

### Sync Matches (Admin)

```bash
curl -X POST "http://localhost:8000/api/v1/matches/sync" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

## Project Structure

```
puck-booking/
├── app/
│   ├── core/           # Core functionality (config, database, security)
│   ├── models/         # SQLAlchemy models (User, Match, Booking)
│   ├── schemas/        # Pydantic schemas
│   ├── crud/           # Database operations
│   ├── routers/        # API endpoints (users, matches, bookings)
│   ├── services/       # External services (hockey API)
│   └── main.py         # FastAPI application
├── Dockerfile          # Docker build configuration
├── docker-compose.yml  # Docker orchestration
├── .dockerignore       # Docker build exclusions
├── requirements.txt    # Python dependencies
├── .env.example        # Environment configuration template
├── create_admin.py     # Admin user creation utility
└── README.md          # This file
```

## Database Schema

### Match Model (Simplified)
- `id`: Primary key
- `external_id`: Unique ID from external API
- `date`: Match date and time
- `name`: Match name (e.g., "Oilers vs Lørenskog")
- `arena`: Venue name (e.g., "DNB Arena")

### User Model
- `id`, `email`, `username`, `hashed_password`
- `is_active`, `is_admin`, `created_at`

### Booking Model
- `id`, `user_id`, `match_id`, `created_at`
- Unique constraint on (user_id, match_id)

## Configuration

Configuration is handled via environment variables or the `.env` file:

- `PROJECT_NAME`: API project name
- `VERSION`: API version
- `API_V1_STR`: API version prefix (default: `/api/v1`)
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT encoding (change in production!)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `HOCKEY_API_URL`: External hockey API endpoint
- `MAX_BOOKINGS_PER_MATCH`: Maximum bookings per match (default: 2)
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated or "*")

## Docker Deployment

### Quick Start with Docker

```bash
# Build and run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Docker Commands

```bash
# Build the image
docker build -t puck-booking:latest .

# Run the container
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -v $(pwd)/data:/app/data \
  --name puck-booking \
  puck-booking:latest

# View logs
docker logs -f puck-booking

# Stop and remove
docker stop puck-booking && docker rm puck-booking
```

### Production with PostgreSQL

Uncomment the PostgreSQL service in `docker-compose.yml` and update the `DATABASE_URL`:

```yaml
# In docker-compose.yml, uncomment the db service
# Then set DATABASE_URL:
DATABASE_URL=postgresql://puckbooking:changeme@db:5432/puckbooking
```

## Business Logic

### Match Syncing

- Admin users can trigger a sync from the external hockey API
- Only matches at "DNB Arena" with "Scheduled" status are imported
- Syncing clears all existing matches and replaces them with fresh data
- Bookings are automatically deleted when matches are cleared (cascade)

### Booking Rules

- Users must be authenticated to create bookings
- Maximum 2 bookings per match (teacher's requirement)
- Users cannot book the same match twice
- Users can delete their own bookings
- Admins can delete any booking

### User Roles

- **Regular Users**: Can register, login, view matches, create/delete own bookings
- **Admin Users**: All user capabilities + sync matches, delete users, view all bookings

Note: The first admin user must be created directly in the database. You can modify a user's `is_admin` field manually or create a script for this.

## Development

### Creating an Admin User

To create the first admin user, you can use a Python script:

```python
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.crud.user import create_user
from app.schemas.user import UserCreate

init_db()
db = SessionLocal()

# Create admin user
admin = UserCreate(
    email="admin@example.com",
    username="admin",
    password="adminpassword"
)
db_admin = create_user(db, admin)
db_admin.is_admin = True
db.commit()
db.close()

print("Admin user created!")
```

## Security Considerations

- Change the `SECRET_KEY` in production
- Use strong passwords
- Consider rate limiting for production
- Use HTTPS in production
- Configure CORS appropriately for your frontend
- Consider using a more robust database (PostgreSQL) for production
- Implement proper logging and monitoring

## Future Enhancements

- Email verification for registration
- Password reset functionality
- Scheduled automatic match syncing (background task)
- Push notifications for booking confirmations
- Booking cancellation policies
- Match capacity management
- User profile management
- Export bookings to CSV/Excel

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
