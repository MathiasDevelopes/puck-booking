from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MatchBase(BaseModel):
    external_id: int
    date: datetime
    name: str
    arena: str


class MatchResponse(MatchBase):
    id: int
    bookings_count: Optional[int] = 0
    is_full: Optional[bool] = False

    class Config:
        from_attributes = True


class ExternalMatchResponse(BaseModel):
    """Schema for external API response."""
    id: int
    date: str
    homeTeam: dict
    awayTeam: dict
    venue: dict
    status: str
    tournament: dict
