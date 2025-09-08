from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import relationship

class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    points = Column(Integer, default=0)
    rank = Column(Integer, nullable=False)
    month = Column(String, nullable=False)

    user = relationship("User", back_populates="leaderboards")


#test korte hobe create er jonno