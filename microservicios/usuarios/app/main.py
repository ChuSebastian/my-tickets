from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app import models, schemas, crud
from .models import User
from sqlalchemy.exc import IntegrityError

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para registrar un nuevo usuario
@app.post("/register", response_model=schemas.UserInDB)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Crear un nuevo usuario en la base de datos
    new_user = crud.create_user(db, user)
    return new_user

# Ruta para hacer login de un usuario
@app.post("/login")
async def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Buscar el usuario por su nombre de usuario
    db_user = crud.get_user_by_username(db, user.username)

    # Verificar si el usuario existe
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Verificar si la contraseña es correcta
    if db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return {"message": "Login successful"}

@app.get("/users", response_model=list[schemas.UserInDB])
async def get_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@app.post("/roles", response_model=schemas.Role)
async def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db, role)

@app.post("/assign-role")
async def assign_role(user_role: schemas.UserRoleCreate, db: Session = Depends(get_db)):
    return crud.assign_role_to_user(db, user_role)
