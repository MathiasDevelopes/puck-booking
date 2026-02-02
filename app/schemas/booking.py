from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.match import MatchResponse
from app.schemas.user import UserResponse


class BookingCreate(BaseModel):
    match_id: int


class BookingResponse(BaseModel):
    id: int
    user_id: int
    match_id: int
    created_at: datetime
    match: Optional[MatchResponse] = None
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True


class BookingListResponse(BaseModel):
    id: int
    match_id: int
    created_at: datetime
    match: MatchResponse

    class Config:
        from_attributes = True
