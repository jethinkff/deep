from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'course_user'

    user_id = Column(String, primary_key=True)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    country = Column(String)
    region = Column(String)
    email_consent = Column(String)
    profession = Column(String)
    primary_area_of_focus = Column(String)
    primary_area_of_focus_other = Column(String)
    practice_setting = Column(String)
    retail_chain = Column(String)
    medical_school = Column(String)
    expected_year_of_residency_completion = Column(String)
    accreditation_cycle_deadline = Column(String)
    license_number = Column(String)
    racgp_number = Column(String)
    acrrm_number = Column(String)
    oaa_number = Column(String)
    psa_number = Column(String)
    acp_number = Column(String)
    rcna_number = Column(String)
    apna_number = Column(String)
    racs_number = Column(String)
    scfhs_classification_id = Column(String)
    ahpra_number = Column(String)
    moh_type = Column(String)
    registered_to_practice_in_australia = Column(String)
    lms_first_access_date = Column(TIMESTAMP)
    lms_last_access_date = Column(TIMESTAMP)
    last_login_date = Column(TIMESTAMP)
    registration_date = Column(TIMESTAMP)
    last_modified_date = Column(TIMESTAMP)
    ingestion_time = Column(TIMESTAMP)
    _PARTITIONTIME = Column(TIMESTAMP, nullable=False)
