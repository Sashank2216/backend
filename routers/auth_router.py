from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from utils.auth_utils import hash_password, verify_password
from utils.token_utils import create_access_token
from schemas.user_schema import SignupSchema, LoginSchema, UserOut
import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=dict)
def signup(payload: SignupSchema, db: Session = Depends(get_db)):
    if payload.role not in ("brand", "influencer"):
        raise HTTPException(status_code=400, detail="role must be 'brand' or 'influencer'")

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        id=str(uuid.uuid4()),
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        tag=payload.tag,
        location=payload.location,
        role=payload.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "signup successful", "user_id": new_user.id}

@router.post("/login", response_model=dict)
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.id, role=user.role)
    return {"access_token": token, "token_type": "bearer"}
