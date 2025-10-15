from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from database import SessionLocal
from sqlalchemy.orm import Session
from models.brand import Brand
from models.influencer import Influencer
from models.user import User
from schemas.brand_schema import BrandCreateUpdate, BrandOut
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

@router.get("/filter", response_model=List[BrandOut])
def filter_brands(name: Optional[str] = None,
                  tag: Optional[str] = None,
                  location: Optional[str] = None,
                  event_date: Optional[str] = None,
                  db: Session = Depends(get_db)):
    q = db.query(Brand).join(User, Brand.user_id == User.id)
    if name:
        q = q.filter(Brand.name.ilike(f"%{name}%"))
    if tag:
        q = q.filter(Brand.tag == tag)
    if location:
        q = q.filter(Brand.location == location)
    if event_date:
        from sqlalchemy import and_, or_
        q = q.filter(Brand.event_start <= event_date).filter(Brand.event_end >= event_date)
    results = q.all()
    return results

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

@router.put("/{brand_id}/update", response_model=BrandOut)
def update_brand(brand_id: str, payload: BrandCreateUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
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

    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        brand = Brand(id=brand_id, user_id=user.id)
        db.add(brand)
        db.commit()
        db.refresh(brand)

    if brand.user_id != user.id:
        raise HTTPException(status_code=403, detail="Cannot update another brand")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(brand, key, value)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand
