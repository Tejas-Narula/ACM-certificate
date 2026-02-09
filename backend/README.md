# ACM Certificate Management System - Backend

A complete backend API for managing and verifying certificates for ACM Club events.

## Features

- **Admin Certificate Management**: Create, update, and delete certificates
- **Certificate Verification**: Public endpoint to verify certificates by code
- **Workshop Management**: Manage workshops/events
- **Admin Authentication**: Secure JWT-based authentication
- **Bulk Operations**: Create multiple certificates at once
- **PostgreSQL Database**: Persistent storage with Supabase compatibility
- **RESTful API**: Clean and intuitive API endpoints

## Quick Setup (Choose One)

### 🚀 Fastest - Supabase (No Installation Required)
For deployment to Render, just use Supabase from the start:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://postgres:PASSWORD@db.XXXXX.supabase.co:5432/postgres
```

Then:
```bash
python init_db.py
python main.py
```

### 💻 Local PostgreSQL (Windows/Mac/Linux)
Use local PostgreSQL without Docker.

See: [LOCAL_SETUP.md](LOCAL_SETUP.md) for step-by-step instructions

### 🐳 Docker (If Installed)
```bash
docker-compose up -d
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python main.py
```

---

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL (local or Supabase)
- pip

### Installation

1. **Navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your database credentials:
   ```env
   # Local PostgreSQL
   DATABASE_URL=postgresql://postgres:password@localhost:5432/acm_certificates
   
   # OR Supabase
   DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
   
   SECRET_KEY=your-secret-key-here
   ADMIN_EMAIL=admin@acmclub.com
   ADMIN_PASSWORD=admin123
   ```

5. **Initialize database**
   ```bash
   python init_db.py
   ```

6. **Run the server**
   ```bash
   python main.py
   ```
   
   Server will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register admin
- `POST /api/auth/login` - Login and get token
- `POST /api/auth/init-admin` - Initialize default admin

### Certificates (Public)
- `GET /api/certificates/verify/{code}` - Verify certificate by code
- `GET /api/certificates/search?email=...` - Search certificates by email

### Certificates (Admin)
- `POST /api/certificates/` - Create certificate
- `GET /api/certificates/admin/all` - Get all certificates
- `GET /api/certificates/admin/{certificate_id}` - Get certificate details
- `PATCH /api/certificates/admin/{certificate_id}` - Update certificate
- `DELETE /api/certificates/admin/{certificate_id}` - Delete certificate
- `POST /api/certificates/admin/bulk-create` - Create multiple certificates
- `GET /api/certificates/admin/stats` - Get statistics

### Workshops (Public)
- `GET /api/workshops/` - Get all workshops
- `GET /api/workshops/{workshop_id}` - Get workshop details

### Workshops (Admin)
- `POST /api/workshops/` - Create workshop
- `PATCH /api/workshops/{workshop_id}` - Update workshop
- `DELETE /api/workshops/{workshop_id}` - Delete workshop

## Database Schema

### Certificates Table
```
- id: UUID (Primary Key)
- code: String (Unique) - Format: ACM-YYYY-XXXXXX
- recipient_name: String
- email: String (Indexed)
- workshop_name: String
- issue_date: String
- skills: JSON (Array)
- instructor: String
- is_verified: Boolean
- verification_code: String (Unique)
- created_at: DateTime
- updated_at: DateTime
```

### Workshops Table
```
- id: UUID (Primary Key)
- title: String (Indexed)
- date: String
- description: Text
- level: String
- instructor: String
- image: String
- created_at: DateTime
- updated_at: DateTime
```

### Admins Table
```
- id: UUID (Primary Key)
- email: String (Unique, Indexed)
- hashed_password: String
- is_active: Boolean
- created_at: DateTime
- updated_at: DateTime
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Login to get token:
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@acmclub.com","password":"admin123"}'
   ```

2. Use token in requests:
   ```bash
   curl -X GET http://localhost:8000/api/certificates/admin/all \
     -H "Authorization: Bearer <your_token>"
   ```

## Usage Examples

### Create a Certificate
```bash
curl -X POST http://localhost:8000/api/certificates/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_name": "John Doe",
    "email": "john@example.com",
    "workshop_name": "React Basics",
    "issue_date": "2024-02-09",
    "skills": ["React", "JavaScript"],
    "instructor": "Dr. Smith"
  }'
```

### Verify a Certificate
```bash
curl http://localhost:8000/api/certificates/verify/ACM-2024-ABC123
```

### Create Multiple Certificates
```bash
curl -X POST http://localhost:8000/api/certificates/admin/bulk-create \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "recipient_name": "Alice",
      "email": "alice@example.com",
      "workshop_name": "Python 101",
      "issue_date": "2024-02-09",
      "skills": ["Python", "OOP"],
      "instructor": "Prof. Johnson"
    },
    {
      "recipient_name": "Bob",
      "email": "bob@example.com",
      "workshop_name": "Python 101",
      "issue_date": "2024-02-09",
      "skills": ["Python", "OOP"],
      "instructor": "Prof. Johnson"
    }
  ]'
```

## Supabase Migration

When switching to Supabase:

1. Get your database URL from Supabase dashboard
2. Update `.env`:
   ```
   DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
   ```
3. The tables will be created automatically on first run

## Development

### Run with auto-reload
```bash
uvicorn main:app --reload --port 8000
```

### Access API documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Directory Structure
```
backend/
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── database.py          # Database setup
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication & JWT
├── crud.py              # Database operations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── routers/
    ├── auth.py         # Authentication routes
    ├── certificates.py # Certificate routes
    └── workshops.py    # Workshop routes
```

## Security Notes

- Change `SECRET_KEY` in `.env` for production
- Use strong passwords for admin accounts
- Enable HTTPS in production
- Implement rate limiting for public endpoints
- Validate email before issuing certificates
- Consider file-based backups alongside database

## License

ACM Club © 2024
