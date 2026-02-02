from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from app.models.match import Match


def get_match_by_id(db: Session, match_id: int) -> Optional[Match]:
    """Get a match by ID."""
    return db.query(Match).filter(Match.id == match_id).first()


def get_match_by_external_id(db: Session, external_id: int) -> Optional[Match]:
    """Get a match by external API ID."""
    return db.query(Match).filter(Match.external_id == external_id).first()


def get_matches(db: Session, skip: int = 0, limit: int = 100) -> List[Match]:
    """Get all matches with pagination."""
    return db.query(Match).order_by(Match.date).offset(skip).limit(limit).all()


def get_upcoming_matches(db: Session, skip: int = 0, limit: int = 100) -> List[Match]:
    """Get upcoming matches only."""
    now = datetime.now(timezone.utc)
    return db.query(Match).filter(Match.date >= now).order_by(Match.date).offset(skip).limit(limit).all()


def create_match(db: Session, match_data: dict) -> Match:
    """Create a new match."""
    db_match = Match(**match_data)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def clear_all_matches(db: Session) -> None:
    """Delete all matches from the database."""
    db.query(Match).delete()
    db.commit()


def bulk_create_matches(db: Session, matches_data: List[dict]) -> List[Match]:
    """Bulk create matches."""
    db_matches = [Match(**match_data) for match_data in matches_data]
    db.add_all(db_matches)
    db.commit()
    for match in db_matches:
        db.refresh(match)
    return db_matches
