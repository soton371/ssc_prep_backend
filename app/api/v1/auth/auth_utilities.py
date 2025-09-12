import jwt
from app.core.setting import settings
from typing import Optional
from datetime import datetime, timedelta, timezone
from app.api.v1.auth.auth_schema import TokenData, Token


def create_access_token(user_id: int, expires_minutes: Optional[int] = None) -> Token:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"user_id": user_id, "exp": expire}  
    return Token(
        access_token=jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256"),
        token_type="bearer"
    )


def verifyAccessToken(token: str) -> TokenData:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = int(payload.get('user_id'))
    return TokenData(id=user_id)
