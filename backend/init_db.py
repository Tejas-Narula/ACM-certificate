"""
Script to initialize database with sample data
Run after starting the server: python init_db.py
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from database import Base, init_db
from models import Workshop, Admin, Certificate
from auth import hash_password
import uuid
from datetime import datetime


def init_sample_data():
    """Initialize database with sample data"""
    init_db()  # Create tables

    from database import SessionLocal

    db = SessionLocal()

    # Check if admin exists
    admin = db.query(Admin).filter(
        Admin.email == settings.ADMIN_EMAIL
    ).first()

    if not admin:
        hashed_pwd = hash_password(settings.ADMIN_PASSWORD)
        admin = Admin(
            email=settings.ADMIN_EMAIL,
            hashed_password=hashed_pwd,
        )
        db.add(admin)
        print(f"✓ Created admin: {settings.ADMIN_EMAIL}")

    # Check if workshops exist
    workshop_count = db.query(Workshop).count()
    if workshop_count == 0:
        workshops = [
            Workshop(
                title="Advanced React Patterns",
                date="October 24, 2023",
                description="Learn advanced React patterns including hooks, context, and performance optimization",
                level="Advanced",
                instructor="Dr. Emily Chen",
                image="/assets/react.jpg",
            ),
            Workshop(
                title="Python for Data Science",
                date="November 10, 2023",
                description="Master Python with Pandas, NumPy, and data visualization",
                level="Intermediate",
                instructor="Prof. Michael Ross",
                image="/assets/python.jpg",
            ),
            Workshop(
                title="Web Development Fundamentals",
                date="November 25, 2023",
                description="Learn HTML, CSS, and JavaScript fundamentals",
                level="Beginner",
                instructor="Sarah Johnson",
                image="/assets/web.jpg",
            ),
        ]
        db.add_all(workshops)
        print(f"✓ Created {len(workshops)} sample workshops")

    # Check if certificates exist
    cert_count = db.query(Certificate).count()
    if cert_count == 0:
        certificates = [
            Certificate(
                code="ACM-2024-REACT001",
                recipient_name="Alex Johnson",
                email="alex@example.com",
                workshop_name="Advanced React Patterns",
                issue_date="October 24, 2023",
                skills=["React Hooks", "Context API", "Performance Optimization"],
                instructor="Dr. Emily Chen",
                verification_code=str(uuid.uuid4()),
            ),
            Certificate(
                code="ACM-2024-PYDS001",
                recipient_name="Sarah Smith",
                email="sarah@example.com",
                workshop_name="Python for Data Science",
                issue_date="November 10, 2023",
                skills=["Pandas", "NumPy", "Matplotlib"],
                instructor="Prof. Michael Ross",
                verification_code=str(uuid.uuid4()),
            ),
        ]
        db.add_all(certificates)
        print(f"✓ Created {len(certificates)} sample certificates")

    db.commit()
    db.close()
    print("\n✓ Database initialization complete!")
    print("\nYou can now test the API:")
    print("- Frontend: http://localhost:5173")
    print("- API Docs: http://localhost:8000/docs")
    print(f"- Default Admin Email: {settings.ADMIN_EMAIL}")
    print(f"- Default Admin Password: {settings.ADMIN_PASSWORD}")
    print("\nTest certificate codes:")
    print("- ACM-2024-REACT001")
    print("- ACM-2024-PYDS001")


if __name__ == "__main__":
    init_sample_data()
