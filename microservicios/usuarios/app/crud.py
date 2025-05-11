from sqlalchemy.orm import Session
from app.models import User, Role, UserRole
from app import schemas

# Crear un nuevo usuario
def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Obtener un usuario por nombre de usuario
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Obtener un usuario por email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Crear rol
def create_role(db: Session, role: schemas.RoleCreate):
    db_role = Role(nombre_rol=role.nombre_rol)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# Asignacion de rol a usuario
def assign_role_to_user(db: Session, user_role: schemas.UserRoleCreate):
    relation = UserRole(usuario_id=user_role.usuario_id, rol_id=user_role.rol_id)
    db.add(relation)
    db.commit()
    return {"message": "Rol asignado correctamente"}

# Obtener todos los usuarios
def get_all_users(db: Session):
    return db.query(User).all()

