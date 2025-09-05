from fastapi import APIRouter
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.db.session import get_db
from app.api.v1.leaderboard import leaderboard_service
from app.api.v1.leaderboard.leaderboard_schema import LeaderboardCreate, LeaderboardResponse

router = APIRouter(
    prefix="/api/v1/leaderboard",
    tags=['Leaderboard']
)

@router.post("/", response_model=LeaderboardResponse)
def create_leaderboard_entry(leaderboard_data: LeaderboardCreate, db: Session = Depends(get_db)):
    try:
        db_entry = leaderboard_service.create_leaderboard_entry(db, leaderboard_data)
        return db_entry
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))