from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from database import SessionLocal
from sqlalchemy.orm import Session
from models.brand import Brand
from models.influencer import Influencer
from models.user import User
from schemas.brand_schema import BrandCreateUpdate, BrandOut, BrandFullOut
from utils.token_utils import decode_token
from fastapi import Header

router = APIRouter(prefix="/brands", tags=["Brands"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    try:
        token_type, token = authorization.split()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/filter", response_model=List[BrandFullOut])
def filter_brands(
    # User table filters
    user_name: Optional[str] = None,
    user_email: Optional[str] = None,
    user_tag: Optional[str] = None,
    user_location: Optional[str] = None,
    user_role: Optional[str] = None,
    # Brand table filters
    brand_name: Optional[str] = None,
    brand_email: Optional[str] = None,
    phone_number: Optional[str] = None,
    brand_tag: Optional[str] = None,
    brand_location: Optional[str] = None,
    event_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Brand, User).join(User, Brand.user_id == User.id)
    # user filters
    if user_name:
        q = q.filter(User.name.ilike(f"%{user_name}%"))
    if user_email:
        q = q.filter(User.email.ilike(f"%{user_email}%"))
    if user_tag:
        q = q.filter(User.tag == user_tag)
    if user_location:
        q = q.filter(User.location == user_location)
    if user_role:
        q = q.filter(User.role == user_role)
    # brand filters
    if brand_name:
        q = q.filter(Brand.name.ilike(f"%{brand_name}%"))
    if brand_email:
        q = q.filter(Brand.email.ilike(f"%{brand_email}%"))
    if phone_number:
        q = q.filter(Brand.phone_number.ilike(f"%{phone_number}%"))
    if brand_tag:
        q = q.filter(Brand.tag == brand_tag)
    if brand_location:
        q = q.filter(Brand.location == brand_location)
    if event_date:
        q = q.filter(Brand.event_start <= event_date).filter(Brand.event_end >= event_date)

    rows = q.all()
    out = []
    for brand, user in rows:
        out.append({
            "user_id": user.id,
            "user_name": user.name,
            "user_email": user.email,
            "user_tag": user.tag,
            "user_location": user.location,
            "user_role": user.role,
            "user_created_at": user.created_at,
            "brand_id": brand.id,
            "brand_name": brand.name,
            "brand_email": brand.email,
            "phone_number": brand.phone_number,
            "brand_tag": brand.tag,
            "brand_location": brand.location,
            "event_start": brand.event_start,
            "event_end": brand.event_end,
        })
    return out

@router.get("/trending", response_model=List[dict])
def trending_influencers(tag: Optional[str] = None, location: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Influencer).join(User, Influencer.user_id == User.id)
    if tag:
        q = q.filter(User.tag == tag)
    if location:
        q = q.filter(User.location == location)
    q = q.order_by(Influencer.reach.desc())
    results = q.all()
    out = []
    for infl in results:
        user = db.query(User).filter(User.id == infl.user_id).first()
        out.append({
            "influencer_id": infl.id,
            "name": user.name if user else None,
            "location": user.location if user else None,
            "tag": user.tag if user else None,
            "reach": infl.reach,
            "verified": infl.verified
        })
    return out

@router.put("/update", response_model=BrandOut)
def update_brand(payload: BrandCreateUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization")
    try:
        token_type, token = authorization.split()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    payload_token = decode_token(token)
    if not payload_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == payload_token.get("sub")).first()
    if not user or user.role != "brand":
        raise HTTPException(status_code=403, detail="Only brand users can update brand profile")
    brand = db.query(Brand).filter(Brand.user_id == user.id).first()
    if not brand:
        brand = Brand(user_id=user.id)
        db.add(brand)
        db.commit()
        db.refresh(brand)

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(brand, key, value)
    if payload.name is not None:
        user.name = payload.name
    if payload.email is not None:
        user.email = payload.email
    if payload.tag is not None:
        user.tag = payload.tag
    if payload.location is not None:
        user.location = payload.location

    db.add(brand)
    db.add(user)
    db.commit()
    db.refresh(brand)
    return brand
