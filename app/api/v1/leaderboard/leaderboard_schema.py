from pydantic import BaseModel
from app.api.v1.auth.auth_schema import UserResponse
    

# For creating new leaderboard entries
class LeaderboardCreate(BaseModel):
    user_id: int
    points: int
    

# For responses
class LeaderboardResponse(LeaderboardCreate):
    id: int
    rank: int
    month: str
    user: UserResponse

    class Config:
        from_attributes = True