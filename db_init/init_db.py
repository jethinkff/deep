from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.course import Base as CourseBase
from models.user import Base as UserBase
from models.user_course_completion import Base as CompletionBase

DATABASE_URL = "postgresql://admin:admin@localhost:5432/datamart"

# Create database engine
engine = create_engine(DATABASE_URL)

# Create tables
# CourseBase.metadata.create_all(engine)
UserBase.metadata.create_all(engine)
# CompletionBase.metadata.create_all(engine)

print("✅ Database and tables initialized successfully!")
