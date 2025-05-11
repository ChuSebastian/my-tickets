from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Tabla intermedia usuarios_roles
class UserRole(Base):
    __tablename__ = "usuarios_roles"
    usuario_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)

# Tabla de roles
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), unique=True, index=True)

    usuarios = relationship("User", secondary="usuarios_roles", back_populates="roles")

# Tabla de usuarios
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)

    roles = relationship("Role", secondary="usuarios_roles", back_populates="usuarios")
