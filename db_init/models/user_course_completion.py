from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserCourseCompletion(Base):
    __tablename__ = 'user_course_completion'

    course_completion_id = Column(Integer, primary_key=True)
    user_id = Column(String)
    course_id = Column(String)
    completion_date = Column(TIMESTAMP)
    ingestion_time = Column(TIMESTAMP)
    _PARTITIONTIME = Column(TIMESTAMP, nullable=False)
