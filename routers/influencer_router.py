from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from database import SessionLocal
from sqlalchemy.orm import Session
from models.influencer import Influencer
from models.brand import Brand
from models.user import User
from schemas.influencer_schema import InfluencerCreateUpdate, InfluencerOut, InfluencerFullOut
from utils.token_utils import decode_token
from fastapi import Header

router = APIRouter(prefix="/influencers", tags=["Influencers"])

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

@router.get("/filter", response_model=List[InfluencerFullOut])
def filter_influencers(
    # User table filters
    user_name: Optional[str] = None,
    user_email: Optional[str] = None,
    user_tag: Optional[str] = None,
    user_location: Optional[str] = None,
    user_role: Optional[str] = None,
    # Influencer table filters
    min_reach: Optional[int] = Query(None, alias="reach"),
    verified: Optional[bool] = None,
    influencer_email: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Influencer, User).join(User, Influencer.user_id == User.id)
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
    if min_reach is not None:
        q = q.filter(Influencer.reach >= min_reach)
    if verified is not None:
        q = q.filter(Influencer.verified == verified)
    if influencer_email:
        q = q.filter(Influencer.email.ilike(f"%{influencer_email}%"))
    rows = q.all()
    out = []
    for infl, user in rows:
        out.append({
            "user_id": user.id,
            "user_name": user.name,
            "user_email": user.email,
            "user_tag": user.tag,
            "user_location": user.location,
            "user_role": user.role,
            "user_created_at": user.created_at,
            "influencer_id": infl.id,
            "reach": infl.reach,
            "verified": infl.verified,
            "influencer_email": infl.email,
        })
    return out

@router.get("/suggestions", response_model=List[dict])
def suggested_brands(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)
    if user.role != "influencer":
        raise HTTPException(status_code=403, detail="Only influencers can access suggestions")

    q = db.query(Brand)
    if user.tag:
        q = q.filter(Brand.tag == user.tag)
    if user.location:
        q = q.filter(Brand.location == user.location)
    results = q.all()
    return results

@router.put("/update", response_model=InfluencerOut)
def update_influencer(payload: InfluencerCreateUpdate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)

    if user.role != "influencer":
        raise HTTPException(status_code=403, detail="Only influencer role can update influencer profile")
    infl = db.query(Influencer).filter(Influencer.user_id == user.id).first()
    if not infl:
        infl = Influencer(user_id=user.id)
        db.add(infl)
        db.commit()
        db.refresh(infl)

    if payload.reach is not None:
        infl.reach = payload.reach
    if payload.verified is not None:
        infl.verified = payload.verified
    if payload.email:
        infl.email = payload.email
    if payload.email is not None:
        user.email = payload.email
    if payload.name is not None:
        user.name = payload.name
    if payload.tag is not None:
        user.tag = payload.tag
    if payload.location is not None:
        user.location = payload.location

    db.add(infl)
    db.add(user)
    db.commit()
    db.refresh(infl)
    return infl

@router.post("/{influencer_id}/verify-reach")
def verify_reach(influencer_id: str, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)
    if user.role != "brand":
        raise HTTPException(status_code=403, detail="Only brand users can request verification (MVP)")
    infl = db.query(Influencer).filter(Influencer.id == influencer_id).first()
    if not infl:
        raise HTTPException(status_code=404, detail="Influencer not found")
    infl.verified = True
    db.add(infl)
    db.commit()
    db.refresh(infl)
    return {"msg": "Influencer reach verified (manual toggle in MVP)", "influencer_id": influencer_id}
