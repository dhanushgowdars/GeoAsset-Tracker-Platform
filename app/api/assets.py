from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from app.services.asset_service import AssetService

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.post("/", response_model=AssetResponse)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    return AssetService.create_asset(db, asset)


@router.get("/", response_model=list[AssetResponse])
def get_assets(db: Session = Depends(get_db)):
    return AssetService.get_all_assets(db)


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = AssetService.get_asset_by_id(db, asset_id)

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return asset


@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    asset_update: AssetUpdate,
    db: Session = Depends(get_db),
):
    db_asset = AssetService.get_asset_by_id(db, asset_id)

    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return AssetService.update_asset(db, db_asset, asset_update)


@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = AssetService.get_asset_by_id(db, asset_id)

    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    AssetService.delete_asset(db, db_asset)

    return {"message": "Asset deleted successfully"}
