from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, index=True, nullable=False)  # ID from external API
    date = Column(DateTime, nullable=False, index=True)
    home_team_id = Column(Integer, nullable=False)
    home_team_full_name = Column(String, nullable=False)
    home_team_short_name = Column(String, nullable=False)
    away_team_id = Column(Integer, nullable=False)
    away_team_full_name = Column(String, nullable=False)
    away_team_short_name = Column(String, nullable=False)
    venue_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    tournament_id = Column(String, nullable=False)
    tournament_name = Column(String, nullable=False)
    
    # Relationships
    bookings = relationship("Booking", back_populates="match", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Match(id={self.id}, external_id={self.external_id}, {self.home_team_short_name} vs {self.away_team_short_name})>"
