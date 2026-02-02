from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse, BookingListResponse
from app.crud import booking as booking_crud
from app.crud import match as match_crud

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new booking for the current user."""
    # Check if match exists
    match = match_crud.get_match_by_id(db, booking.match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    # Check if user already booked this match
    if booking_crud.check_user_already_booked(db, current_user.id, booking.match_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already booked this match"
        )
    
    # Check if match is full
    if booking_crud.is_match_full(db, booking.match_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This match is already fully booked (max 2 bookings)"
        )
    
    # Create booking
    db_booking = booking_crud.create_booking(db, current_user.id, booking.match_id)
    return db_booking


@router.get("/my-bookings", response_model=List[BookingListResponse])
def get_my_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all bookings for the current user."""
    bookings = booking_crud.get_user_bookings(db, current_user.id, skip, limit)
    return bookings


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a booking. Users can delete their own bookings."""
    booking = booking_crud.get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check if user owns this booking or is admin
    if booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this booking"
        )
    
    booking_crud.delete_booking(db, booking_id)
    return None


@router.get("/", response_model=List[BookingResponse])
def list_all_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all bookings (Admin only)."""
    bookings = booking_crud.get_all_bookings(db, skip, limit)
    return bookings


@router.get("/match/{match_id}", response_model=List[BookingResponse])
def get_match_bookings(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all bookings for a specific match."""
    match = match_crud.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    bookings = booking_crud.get_match_bookings(db, match_id)
    return bookings
