from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, index=True, nullable=False)  # ID from external API
    date = Column(DateTime, nullable=False, index=True)
    name = Column(String, nullable=False)  # Match name (e.g., "Oilers vs Lørenskog")
    arena = Column(String, nullable=False)  # Venue name
    
    # Relationships
    bookings = relationship("Booking", back_populates="match", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Match(id={self.id}, name={self.name}, arena={self.arena})>"
