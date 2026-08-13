from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/deals", tags=["deals"])


@router.get("", response_model=List[schemas.DealOut])
def list_deals(db: Session = Depends(get_db), _=Depends(auth.get_current_user)):
    return db.query(models.Deal).all()


@router.post("", response_model=schemas.DealOut)
def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_deal = models.Deal(**deal.model_dump(), owner_id=current_user.id)
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal


@router.get("/{deal_id}", response_model=schemas.DealOut)
def get_deal(deal_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_user)):
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.patch("/{deal_id}", response_model=schemas.DealOut)
def update_deal(deal_id: int, update: schemas.DealUpdate, db: Session = Depends(get_db), _=Depends(auth.get_current_user)):
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(deal, field, value)
    db.commit()
    db.refresh(deal)
    return deal


@router.delete("/{deal_id}")
def delete_deal(deal_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_user)):
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    db.delete(deal)
    db.commit()
    return {"ok": True}
