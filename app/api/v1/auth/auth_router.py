from typing import Union, Dict, Any
from sqlalchemy.orm import Session
from app.api.v1.auth import auth_service
from app.api.v1.auth.auth_schema import UserCreate, UserResponse
from app.db.session import get_db
from fastapi import Depends

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
        db_user, access_token = auth_service.login_or_register_user(db, user)

        return {
            "data": UserResponse.model_validate(db_user).model_dump(),
            "access_token": access_token,
            "token_type": "bearer",
        }
    except Exception as e:
        return {"error": str(e)}
