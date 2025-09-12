from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.api.v1.auth.auth_model import User
from app.api.v1.auth.auth_schema import UserCreate, UserResponse, Token
from app.api.v1.auth.auth_utilities import create_access_token
from app.api.v1.leaderboard.leaderboard_schema import LeaderboardCreate
from app.api.v1.leaderboard.leaderboard_service import create_leaderboard_entry

#get_user_by_id
def get_user_by_id(db: Session, user_id: int) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    return db_user

#get_user_by_email
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

#create_user
def create_user(db: Session, user_data: UserCreate) -> User:
    db_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        profile_image=user_data.profile_image,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#login_or_register_user
def login_or_register_user(db: Session, user_data: UserCreate) -> Tuple[UserResponse, Token]:
    db_user = get_user_by_email(db, user_data.email)
    if not db_user:
        db_user = create_user(db, user_data)
        create_leaderboard_entry(db, LeaderboardCreate(user_id=db_user.id, points=0))
    else:
        db_user.full_name = user_data.full_name
        db_user.profile_image = user_data.profile_image
        db.commit()
        db.refresh(db_user)
        # when google login, update user info

    return db_user, create_access_token(user_id=int(db_user.id))

