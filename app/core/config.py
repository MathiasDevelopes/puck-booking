from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "Hockey Booking API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./hockey_booking.db"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External API
    HOCKEY_API_URL: str = "https://oilers.hockeydata.no/live/match?provider=automatic"
    
    # Booking constraints
    MAX_BOOKINGS_PER_MATCH: int = 2
    
    # CORS
    CORS_ORIGINS: str = "*"  # Comma-separated list, or "*" for all origins
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Warn if using default SECRET_KEY
if settings.SECRET_KEY == "your-secret-key-change-in-production":
    import warnings
    warnings.warn(
        "Using default SECRET_KEY. This is insecure for production! "
        "Set SECRET_KEY environment variable.",
        UserWarning
    )
