from fastapi import FastAPI

from app.api.assets import router as asset_router
from app.database.session import test_connection

app = FastAPI(
    title="GeoAsset Tracker Platform",
    description="A production-style backend for managing geospatial assets.",
    version="1.0.0",
)

# Register API routes
app.include_router(asset_router)


@app.get("/")
def root():
    return {"message": "Welcome to GeoAsset Tracker Platform"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-test")
def database_test():
    return {"database": test_connection()}
