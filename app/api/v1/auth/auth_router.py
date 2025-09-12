from typing import Dict, Any
from sqlalchemy.orm import Session
from app.api.v1.auth import auth_service
from app.api.v1.auth.auth_schema import UserCreate, UserResponse, TokenData
from app.db.session import get_db
from fastapi import Depends
from app.api.dependencies import get_current_user
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/auth",
    tags=['Auths']
)


# @router.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


@router.post("/login", response_model=Dict[str, Any])
def login_or_register(user: UserCreate, db: Session = Depends(get_db)) -> Dict[str, Any]:

    try:
        db_user, token = auth_service.login_or_register_user(db, user)

        return {
            "data": UserResponse.model_validate(db_user).model_dump(),
            "access_token": token.access_token,
            "token_type": token.token_type or "bearer",
        }
    except Exception as e:
        return {"error": str(e)}


# get user
@router.get("/profile", response_model=UserResponse)
def get_profile(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)) -> UserResponse:
    try:
        db_user = auth_service.get_user_by_id(db, current_user.id)
        return UserResponse.model_validate(db_user)
    except Exception as e:
        return {"error": str(e)}
