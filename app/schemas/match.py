from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TeamInfo(BaseModel):
    id: int
    full_name: str
    short_name: str


class MatchBase(BaseModel):
    external_id: int
    date: datetime
    home_team_id: int
    home_team_full_name: str
    home_team_short_name: str
    away_team_id: int
    away_team_full_name: str
    away_team_short_name: str
    venue_name: str
    status: str
    tournament_id: str
    tournament_name: str


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
