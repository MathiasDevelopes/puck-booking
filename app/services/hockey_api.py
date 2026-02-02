import httpx
import logging
from typing import List, Dict, Optional
from datetime import datetime
from app.core.config import settings

# Set up logging
logger = logging.getLogger(__name__)


class HockeyAPIService:
    """Service for interacting with the external hockey API."""
    
    def __init__(self):
        self.api_url = settings.HOCKEY_API_URL
        self.timeout = 10.0
    
    async def fetch_matches(self) -> List[Dict]:
        """Fetch matches from the external API."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.api_url)
                response.raise_for_status()
                data = response.json()
                
                # The API returns a single match object, not a list
                # Wrap it in a list for consistent processing
                if isinstance(data, dict):
                    return [data]
                return data if isinstance(data, list) else []
        except httpx.HTTPError as e:
            logger.error(f"Error fetching matches from external API: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return []
    
    def filter_valid_matches(self, matches: List[Dict]) -> List[Dict]:
        """Filter matches to only include DNB Arena and Scheduled status."""
        valid_matches = []
        for match in matches:
            venue = match.get("venue", {})
            venue_name = venue.get("name", "")
            status = match.get("status", "")
            
            if venue_name == "DNB Arena" and status == "Scheduled":
                valid_matches.append(match)
        
        return valid_matches
    
    def transform_match_data(self, external_match: Dict) -> Dict:
        """Transform external API match data to internal format."""
        home_team = external_match.get("homeTeam", {})
        away_team = external_match.get("awayTeam", {})
        venue = external_match.get("venue", {})
        
        # Parse the date string to datetime
        date_str = external_match.get("date", "")
        match_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        
        # Create match name from teams
        match_name = f"{home_team.get('shortName', 'Home')} vs {away_team.get('shortName', 'Away')}"
        
        return {
            "external_id": external_match.get("id"),
            "date": match_date,
            "name": match_name,
            "arena": venue.get("name", "Unknown Arena"),
        }
    
    async def get_valid_matches_for_sync(self) -> List[Dict]:
        """Get all valid matches ready for database sync."""
        matches = await self.fetch_matches()
        valid_matches = self.filter_valid_matches(matches)
        return [self.transform_match_data(match) for match in valid_matches]


hockey_api_service = HockeyAPIService()
