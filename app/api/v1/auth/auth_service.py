from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.api.v1.auth.auth_model import User
from app.api.v1.auth.auth_schema import UserCreate, UserUpdate, UserResponse, Token
from app.api.v1.auth.auth_utilities import create_access_token

#get_user_by_id
def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

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

#update_user
def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise ValueError("User not found")

    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

#delete_user
def delete_user(db: Session, user_id: int) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise ValueError("User not found")

    db.delete(db_user)
    db.commit()
    return db_user


#login_or_register_user
def login_or_register_user(db: Session, user_data: UserCreate) -> Tuple[UserResponse, Token]:

    db_user = get_user_by_email(db, user_data.email)
    if not db_user:
        db_user = create_user(db, user_data)

    return db_user, create_access_token(user_id=int(db_user.id))

# next task auth check