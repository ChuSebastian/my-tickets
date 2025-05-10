import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)

# Nombre de la base de datos
DB_NAME = "usuarios_mysql"

# URL sin especificar base de datos
DB_ROOT_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"

# Crear la base de datos si no existe
engine_root = create_engine(DB_ROOT_URL, echo=True)
with engine_root.connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
    print(f"Base de datos '{DB_NAME}' verificada o creada.")
    connection.commit()

# Ahora sí, conexión a la base de datos real
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
