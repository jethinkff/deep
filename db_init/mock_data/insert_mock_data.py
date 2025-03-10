import pandas as pd
from sqlalchemy import create_engine

# Database connection details
DATABASE_URL = "postgresql://admin:admin@localhost:5432/datamart"
engine = create_engine(DATABASE_URL)

# Load CSV files
# courses_df = pd.read_csv("mock_courses.csv")
users_df = pd.read_csv("mock_users.csv")
# completions_df = pd.read_csv("mock_user_completions.csv")

# Insert data into PostgreSQL
# courses_df.to_sql("course", engine, if_exists="append", index=False)
users_df.to_sql("course_user", engine, if_exists="append", index=False)
# completions_df.to_sql("user_course_completion", engine, if_exists="append", index=False)

print("✅ Data successfully inserted into PostgreSQL!")
