from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "Hockey Booking API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./hockey_booking.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External API
    HOCKEY_API_URL: str = "https://oilers.hockeydata.no/live/match?provider=automatic"
    
    # Booking constraints
    MAX_BOOKINGS_PER_MATCH: int = 2
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
