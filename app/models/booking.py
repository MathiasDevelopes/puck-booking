from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    match = relationship("Match", back_populates="bookings")
    
    # Ensure a user can only book the same match once
    __table_args__ = (UniqueConstraint('user_id', 'match_id', name='_user_match_uc'),)

    def __repr__(self):
        return f"<Booking(id={self.id}, user_id={self.user_id}, match_id={self.match_id})>"
