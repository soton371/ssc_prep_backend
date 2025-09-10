from sqlalchemy.orm import Session, joinedload
from app.api.v1.leaderboard.leaderboard_model import Leaderboard
from app.api.v1.leaderboard.leaderboard_schema import LeaderboardCreate
from app.core.utilities import current_month
from typing import List

# create first leaderboard entry for a user
def create_leaderboard_entry(db: Session, leaderboard_data: LeaderboardCreate) -> Leaderboard:
    # find current rank based on existing entries for the month
    existing_entries = db.query(Leaderboard).filter(
        Leaderboard.month == current_month()).order_by(Leaderboard.rank).all()
    if existing_entries:
        highest_rank = existing_entries[-1].rank
        new_rank = highest_rank + 1
    else:
        new_rank = 1
    db_entry = Leaderboard(
        user_id=leaderboard_data.user_id,
        points=leaderboard_data.points,
        rank=new_rank,
        month=current_month(),  # always current month (e.g., "September")
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# get leaderboard by user_id
def get_leaderboard_by_user_id(db: Session, user_id: int) -> Leaderboard:
    return db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()

# get all leaderboard entries for the current month. and limit skip for pagination and order by rank
def get_leaderboard_for_current_month(db: Session, skip: int = 0, limit: int = 50) -> List[Leaderboard]:
    return db.query(Leaderboard).options(joinedload(Leaderboard.user)).filter(Leaderboard.month == current_month()).order_by(Leaderboard.rank.asc()).offset(skip).limit(limit).all()
