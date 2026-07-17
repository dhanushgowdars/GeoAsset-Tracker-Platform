from fastapi import FastAPI

app = FastAPI(
    title="GeoAsset Tracker Platform",
    description="A production-style backend for managing geospatial assets.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to GeoAsset Tracker Platform"}


@app.get("/health")
def health():
    return {"status": "healthy"}
