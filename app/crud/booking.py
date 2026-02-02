from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.models.booking import Booking
from app.models.match import Match
from app.core.config import settings


def get_booking_by_id(db: Session, booking_id: int) -> Optional[Booking]:
    """Get a booking by ID."""
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_user_bookings(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Booking]:
    """Get all bookings for a user."""
    return db.query(Booking).filter(Booking.user_id == user_id).offset(skip).limit(limit).all()


def get_match_bookings(db: Session, match_id: int) -> List[Booking]:
    """Get all bookings for a match."""
    return db.query(Booking).filter(Booking.match_id == match_id).all()


def get_match_bookings_count(db: Session, match_id: int) -> int:
    """Get the count of bookings for a match."""
    return db.query(Booking).filter(Booking.match_id == match_id).count()


def check_user_already_booked(db: Session, user_id: int, match_id: int) -> bool:
    """Check if a user has already booked a match."""
    booking = db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.match_id == match_id
    ).first()
    return booking is not None


def is_match_full(db: Session, match_id: int) -> bool:
    """Check if a match has reached the maximum bookings."""
    count = get_match_bookings_count(db, match_id)
    return count >= settings.MAX_BOOKINGS_PER_MATCH


def create_booking(db: Session, user_id: int, match_id: int) -> Booking:
    """Create a new booking."""
    db_booking = Booking(user_id=user_id, match_id=match_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def delete_booking(db: Session, booking_id: int) -> bool:
    """Delete a booking by ID."""
    booking = get_booking_by_id(db, booking_id)
    if booking:
        db.delete(booking)
        db.commit()
        return True
    return False


def get_all_bookings(db: Session, skip: int = 0, limit: int = 100) -> List[Booking]:
    """Get all bookings (admin only)."""
    return db.query(Booking).offset(skip).limit(limit).all()
