from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth, ai
from ..database import get_db

router = APIRouter(prefix="/deals", tags=["ai"])


def _get_deal_and_notes(deal_id: int, db: Session):
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    activities = db.query(models.Activity).filter(models.Activity.deal_id == deal_id).all()
    notes = [a.content for a in activities]
    return deal, notes


@router.post("/{deal_id}/summarize")
def summarize_deal(deal_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_user)):
    deal, notes = _get_deal_and_notes(deal_id, db)
    summary = ai.summarize_deal(deal.title, notes)
    return {"deal_id": deal_id, "summary": summary}


@router.post("/{deal_id}/next-steps")
def next_steps(deal_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_user)):
    deal, notes = _get_deal_and_notes(deal_id, db)
    steps = ai.suggest_next_steps(deal.title, notes)
    return {"deal_id": deal_id, "next_steps": steps}


@router.post("/{deal_id}/qualify", response_model=List[schemas.QualificationOut])
def qualify_deal(deal_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    deal, notes = _get_deal_and_notes(deal_id, db)
    results = ai.qualify_deal(deal.title, notes)

    saved = []
    for r in results:
        q = models.Qualification(
            deal_id=deal_id,
            criterion=r.get("criterion", "unknown"),
            confirmed=bool(r.get("confirmed", False)),
            score=int(r.get("score", 0)),
            notes=r.get("notes", ""),
            assessed_by=current_user.id,
        )
        db.add(q)
        saved.append(q)

    db.commit()
    for q in saved:
        db.refresh(q)
    return saved


@router.get("/{deal_id}/qualifications", response_model=List[schemas.QualificationOut])
def get_qualifications(deal_id: int, db: Session = Depends(get_db), _=Depends(auth.get_current_user)):
    return db.query(models.Qualification).filter(models.Qualification.deal_id == deal_id).order_by(models.Qualification.assessed_at.desc()).all()
