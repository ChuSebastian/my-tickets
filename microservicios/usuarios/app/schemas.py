from pydantic import BaseModel

# --- Usuario ---

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(UserCreate):
    id: int

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

# --- Rol ---

class RoleBase(BaseModel):
    nombre_rol: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True

# --- Relación Usuario-Rol ---

class UserRoleCreate(BaseModel):
    usuario_id: int
    rol_id: int
