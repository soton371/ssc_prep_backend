from pydantic import BaseModel
from app.api.v1.auth.auth_schema import UserResponse
    

# For creating new leaderboard entries
class LeaderboardCreate(BaseModel):
    user_id: int
    points: int
    
#For update points
class LeaderboardUpdate(BaseModel):
    points: int

# For responses
class LeaderboardResponse(BaseModel):
    id: int
    points: int
    rank: int
    month: str
    user: UserResponse

    class Config:
        from_attributes = True


# For responses by user_id
class LeaderboardUserResponse(BaseModel):
    id: int
    points: int
    rank: int
    month: str

    class Config:
        from_attributes = True

