from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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

# Obtener todos los usuarios
def get_all_users(db: Session):
    return db.query(User).all()

# Crear un nuevo rol
def create_role(db: Session, role: schemas.RoleCreate):
    db_role = Role(nombre_rol=role.nombre_rol)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# Obtener todos los roles
def get_all_roles(db: Session):
    return db.query(Role).all()

# Obtener un rol por nombre
def get_role_by_name(db: Session, nombre_rol: str):
    return db.query(Role).filter(Role.nombre_rol == nombre_rol).first()

# Asignar rol a usuario con IDs
def assign_role_to_user(db: Session, user_role: schemas.UserRoleCreate):
    relation = UserRole(usuario_id=user_role.usuario_id, rol_id=user_role.rol_id)
    db.add(relation)
    db.commit()
    return {"message": "Rol asignado correctamente"}

# Asignar rol a usuario por nombre, evitando duplicados
def assign_role_to_user_by_name(db: Session, user: User, role_name: str):
    role = get_role_by_name(db, role_name)
    if not role:
        return {"error": f"El rol '{role_name}' no existe."}
    exists = db.query(UserRole).filter_by(usuario_id=user.id, rol_id=role.id).first()
    if not exists:
        db.add(UserRole(usuario_id=user.id, rol_id=role.id))
        db.commit()
    return {"message": f"Rol '{role_name}' asignado a {user.username}"}
