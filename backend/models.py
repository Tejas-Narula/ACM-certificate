from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, Boolean, Table, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import uuid

# Association table for many-to-many relationship between workshops and certificates
workshop_certificate = Table(
    'workshop_certificate',
    Base.metadata,
    Column('workshop_id', String, ForeignKey('workshops.id')),
    Column('certificate_id', String, ForeignKey('certificates.id'))
)


class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False, index=True)
    date = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    level = Column(String, nullable=False, default="Beginner")  # Beginner, Intermediate, Advanced
    instructor = Column(String, nullable=False)
    image = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    certificates = relationship(
        "Certificate",
        secondary=workshop_certificate,
        back_populates="workshops"
    )

    def __repr__(self):
        return f"<Workshop(id={self.id}, title={self.title})>"


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # Format: ACM-YYYY-CODE (e.g., ACM-2024-REACT)
    code = Column(String, unique=True, nullable=False, index=True)
    
    recipient_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    workshop_name = Column(String, nullable=False)
    issue_date = Column(String, nullable=False)
    skills = Column(JSON, default=list)  # List of skills
    instructor = Column(String, nullable=False)
    
    is_verified = Column(Boolean, default=True)
    verification_code = Column(String, unique=True, nullable=False, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workshops = relationship(
        "Workshop",
        secondary=workshop_certificate,
        back_populates="certificates"
    )

    def __repr__(self):
        return f"<Certificate(id={self.id}, code={self.code})>"


class Admin(Base):
    __tablename__ = "admins"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Admin(id={self.id}, email={self.email})>"
