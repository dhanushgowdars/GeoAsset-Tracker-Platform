from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.location_history import router as location_history_router
from app.api.dashboard import router as dashboard_router
from app.api.assets import router as asset_router
from app.database.session import test_connection

from app.api.users import router as user_router

app = FastAPI(
    title="GeoAsset Tracker Platform",
    description="A production-style backend for managing geospatial assets.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(asset_router)
app.include_router(user_router)
app.include_router(dashboard_router)
app.include_router(location_history_router)

@app.get("/")
def root():
    return {"message": "Welcome to GeoAsset Tracker Platform"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-test")
def database_test():
    return {"database": test_connection()}
