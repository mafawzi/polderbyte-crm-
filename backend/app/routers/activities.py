from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth, ai
from ..database import get_db

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/deal/{deal_id}", response_model=List[schemas.ActivityOut])
def list_activities_for_deal(deal_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_user)):
    return db.query(models.Activity).filter(models.Activity.deal_id == deal_id).order_by(models.Activity.created_at.desc()).all()


@router.post("", response_model=schemas.ActivityOut)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    deal = db.query(models.Deal).filter(models.Deal.id == activity.deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    # Auto-summarize on creation so the AI brief is always fresh
    try:
        summary = ai.summarize_activity(activity.content)
    except Exception:
        summary = None  # don't block activity creation if Claude call fails

    db_activity = models.Activity(
        deal_id=activity.deal_id,
        type=activity.type,
        content=activity.content,
        ai_summary=summary,
        created_by=current_user.id,
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_user)):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(activity)
    db.commit()
    return {"ok": True}
