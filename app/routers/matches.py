from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_admin_user
from app.schemas.match import MatchResponse
from app.crud import match as match_crud
from app.crud import booking as booking_crud
from app.services.hockey_api import hockey_api_service

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.get("/", response_model=List[MatchResponse])
def list_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all upcoming matches."""
    matches = match_crud.get_upcoming_matches(db, skip=skip, limit=limit)
    
    # Add bookings count and is_full status
    result = []
    for match in matches:
        bookings_count = booking_crud.get_match_bookings_count(db, match.id)
        match_dict = {
            **match.__dict__,
            "bookings_count": bookings_count,
            "is_full": booking_crud.is_match_full(db, match.id)
        }
        result.append(match_dict)
    
    return result


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(match_id: int, db: Session = Depends(get_db)):
    """Get a specific match by ID."""
    match = match_crud.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    bookings_count = booking_crud.get_match_bookings_count(db, match.id)
    match_dict = {
        **match.__dict__,
        "bookings_count": bookings_count,
        "is_full": booking_crud.is_match_full(db, match.id)
    }
    
    return match_dict


@router.post("/sync", status_code=status.HTTP_200_OK)
async def sync_matches(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Sync matches from external API (Admin only). Clears existing matches and adds new ones."""
    try:
        # Fetch valid matches from external API
        matches_data = await hockey_api_service.get_valid_matches_for_sync()
        
        # Clear existing matches
        match_crud.clear_all_matches(db)
        
        # Bulk create new matches
        if matches_data:
            match_crud.bulk_create_matches(db, matches_data)
        
        return {
            "message": "Matches synced successfully",
            "count": len(matches_data)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error syncing matches: {str(e)}"
        )
