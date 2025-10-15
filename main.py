# main.py
from fastapi import FastAPI
from database import engine, Base
from routers import auth_router, influencer_router, brand_router
import models.user, models.influencer, models.brand  # ensure models are imported for metadata

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Brand-Influencer Connector API")

app.include_router(auth_router.router)
app.include_router(influencer_router.router)
app.include_router(brand_router.router)

@app.get("/")
def root():
    return {"message": "Brand-Influencer Connector API is running"}
