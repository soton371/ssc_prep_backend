from fastapi import APIRouter
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.api.v1.leaderboard import leaderboard_service
from app.api.v1.leaderboard.leaderboard_schema import LeaderboardUpdate
from app.api.v1.auth.auth_schema import TokenData
from app.api.dependencies import get_current_user
from app.core.response import response_success


router = APIRouter(
    prefix="/api/v1/leaderboard",
    tags=['Leaderboard']
)

# @router.post("/", response_model=LeaderboardResponse)
# def create_leaderboard_entry(leaderboard_data: LeaderboardCreate, db: Session = Depends(get_db)):
#     try:
#         db_entry = leaderboard_service.create_leaderboard_entry(db, leaderboard_data)
#         return db_entry
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# for get leaderboard entries for the current month
@router.get("")
def get_leaderboard_by_current_month(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    db_entry = leaderboard_service.get_leaderboard_for_current_month(
        db=db, skip=skip, limit=limit)
    return response_success(data=db_entry)


# get leaderboard entry by user_id
@router.get("/user")
def get_leaderboard_by_user(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    db_entry = leaderboard_service.get_leaderboard_by_user_id(
        db, current_user.id)
    return response_success(data=db_entry)


# update leaderboard entry (increment points) - only for the current user
@router.put("")
def update_leaderboard_entry(gained_points: LeaderboardUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    db_entry = leaderboard_service.update_leaderboard_entry(
        db, current_user.id, gained_points)
    return response_success(data=db_entry)
