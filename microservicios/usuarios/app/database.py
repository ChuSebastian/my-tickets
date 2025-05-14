import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Credentials
MYSQL_USER = "root"
MYSQL_PASSWORD = "utec"
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost") 
MYSQL_PORT = "3306"
DB_NAME = "db_usuarios"

# Build database URL
DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DB_NAME}"
)

# Create engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
