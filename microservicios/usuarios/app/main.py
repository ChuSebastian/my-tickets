from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app import crud, schemas
from app.seed import run_seed
from contextlib import asynccontextmanager

# --- Lifespan para seeding inicial ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    run_seed(db)
    db.close()
    yield

app = FastAPI(lifespan=lifespan)

# --- Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Crear tablas ---
Base.metadata.create_all(bind=engine)

# --- Dependencia de DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---

@app.post("/register", response_model=schemas.UserInDB)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db, user)
    crud.assign_role_to_user_by_name(db, new_user, "viewer")
    return new_user

@app.post("/login")
async def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"message": "Login successful"}

@app.get("/users", response_model=list[schemas.UserOut])
async def get_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@app.post("/roles", response_model=schemas.Role)
async def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db, role)

@app.get("/roles", response_model=list[schemas.Role])
async def get_all_roles(db: Session = Depends(get_db)):
    return crud.get_all_roles(db)

@app.post("/assign-role")
async def assign_role(user_role: schemas.UserRoleCreate, db: Session = Depends(get_db)):
    return crud.assign_role_to_user(db, user_role)
