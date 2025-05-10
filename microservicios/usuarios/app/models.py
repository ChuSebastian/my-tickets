from sqlalchemy import Column, Integer, String
from app.database import Base


# Definición del modelo User que representa la tabla de usuarios en la base de datos
class User(Base):
    __tablename__ = "users"  # Nombre de la tabla

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)  # ID único de cada usuario
    username = Column(
        String(100), unique=True, index=True, nullable=False
    )  # Nombre de usuario único
    email = Column(String(200), nullable=False)  # Email único
    password = Column(
        String(200), nullable=False
    )  # Contraseña sin encriptación por ahora
