from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from database import Base


# Basic Details Table
class BasicDetails(Base):
    __tablename__ = "basic_details"

    basic_details_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    email_address = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    image_url = Column(String(200), nullable=True)
    summary = Column(String(500), nullable=False)
    date_applied = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    location_details = relationship("LocationDetails", backref="basic_details", lazy=True)
    social_media = relationship("SocialMedia", backref="basic_details", lazy=True)
    work_details = relationship("Work", backref="basic_details", lazy=True)
    education_details = relationship("Education", backref="basic_details", lazy=True)
    skills = relationship("Skills", backref="basic_details", lazy=True)
    projects = relationship("Projects", backref="basic_details", lazy=True)

    def __str__(self):
        return self.name


# Location Details Table
class LocationDetails(Base):
    __tablename__ = "location_details"

    id = Column(Integer, primary_key=True, nullable=False)
    basic_details_id = Column(
        Integer,
        ForeignKey("basic_details.basic_details_id", ondelete="CASCADE"),
        nullable=False,
    )
    address_line = Column(String(200), nullable=False)
    street_name = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)


# Social Media Table
class SocialMedia(Base):
    __tablename__ = "social_media"

    id = Column(Integer, primary_key=True, nullable=False)
    basic_details_id = Column(
        Integer,
        ForeignKey("basic_details.basic_details_id", ondelete="CASCADE"),
        nullable=False,
    )
    network = Column(String(100), nullable=True)
    user_name = Column(String(100), nullable=True)
    url = Column(String(250), nullable=True)


# Work experience table
class Work(Base):
    __tablename__ = "work_experience"
    id = Column(Integer, primary_key=True, nullable=False)
    basic_details_id = Column(
        Integer,
        ForeignKey("basic_details.basic_details_id", ondelete="CASCADE"),
        nullable=False,
    )
    organisation = Column(String(200), nullable=True)
    job_role = Column(String(100), nullable=True)
    key_roles = Column(String(500), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)


# Education details table
class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, nullable=False)
    basic_details_id = Column(
        Integer,
        ForeignKey("basic_details.basic_details_id", ondelete="CASCADE"),
        nullable=False,
    )
    qualification = Column(String(100), nullable=False)
    course_name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    institute_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)


# Skill table
class Skills(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, nullable=False)
    basic_details_id = Column(
        Integer,
        ForeignKey("basic_details.basic_details_id", ondelete="CASCADE"),
        nullable=False,
    )
    skill = Column(String(50), nullable=False)
    rating = Column(String(30), nullable=False)


# Projects table
class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, nullable=False)
    basic_details_id = Column(
        Integer,
        ForeignKey("basic_details.basic_details_id", ondelete="CASCADE"),
        nullable=False,
    )
    project_title = Column(String(100), nullable=True)
    skills = Column(String(50), nullable=True)
    description = Column(String(500), nullable=True)
