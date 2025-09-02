from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User

router = APIRouter()

@router.post("/register")
async def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # TODO: Implementar registro de usuario
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario o correo ya existe")

    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado correctamente", "user_id": new_user.id}


@router.post("/login")
async def login_user(email: str, password: str, db: Session = Depends(get_db)):
    # TODO: Implementar login de usuario
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    return {"message": "Login exitoso", "user_id": user.id, "username": user.username}


@router.get("/profile")
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar obtener perfil de usuario
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at
    }


@router.put("/profile")
async def update_user_profile(user_id: int, username: str = None, email: str = None, db: Session = Depends(get_db)):
    # TODO: Implementar actualizar perfil de usuario
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    if username:
        user.username = username
    if email:
        user.email = email

    db.commit()
    db.refresh(user)

    return {"message": "Perfil actualizado correctamente", "user": {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active
    }}
