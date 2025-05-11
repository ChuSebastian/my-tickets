from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app import models, schemas, crud
from .models import User
from sqlalchemy.exc import IntegrityError

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS para permitir cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

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
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = crud.create_user(db, user)
    return new_user

# Ruta para hacer login de un usuario
@app.post("/login")
async def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or db_user.password != user.password:
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
