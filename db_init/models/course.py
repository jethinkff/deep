from sqlalchemy import Column, String, TIMESTAMP, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'course'

    course_id = Column(String, primary_key=True)
    course_name = Column(String)
    start_date = Column(TIMESTAMP)
    end_date = Column(TIMESTAMP)
    create_date = Column(TIMESTAMP)
    last_modified_date = Column(TIMESTAMP)
    course_category_id = Column(String)
    profession_id = Column(String)
    learning_type_id = Column(String)
    accreditation_type_id = Column(String)
    accreditation_expiry_date = Column(TIMESTAMP)
    accreditation_file_number = Column(String)
    sponsor_id = Column(String)
    region_id = Column(String)
    project_code = Column(String)
    duration = Column(String)
    credits = Column(String)
    report_group = Column(String)
    participation_target = Column(String)
    deal_id = Column(String)
    learning_category_id = Column(String)
    ingestion_time = Column(TIMESTAMP)
    hide_in_reporting = Column(Boolean)
    _PARTITIONTIME = Column(TIMESTAMP, nullable=False)
