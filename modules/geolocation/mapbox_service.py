"""
Service Mapbox
Géolocalisation et cartographie
"""
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class MapboxService:
    """
    Intégration Mapbox
    - Geocoding
    - Maps
    - Directions
    """
    
    def __init__(self):
        self.enabled = False
        self._initialize()
    
    def _initialize(self):
        """Initialise Mapbox"""
        from config.settings import Config
        keys = Config.get_api_keys()
        
        self.access_token = keys['mapbox']['access_token']
        self.enabled = self.access_token is not None
        
        if self.enabled:
            logger.info("✓ Mapbox activé")
        else:
            logger.warning("✗ Mapbox token manquant")
    
    def geocode(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Convertit une adresse en coordonnées
        
        Args:
            address: Adresse à géocoder
        
        Returns:
            Coordonnées ou None
        """
        if not self.enabled:
            logger.error("Mapbox non activé")
            return None
        
        try:
            import requests
            
            url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
            params = {
                'access_token': self.access_token,
                'limit': 1
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data['features']:
                feature = data['features'][0]
                coords = feature['geometry']['coordinates']
                
                logger.info(f"✓ Géocodage: {address}")
                
                return {
                    'longitude': coords[0],
                    'latitude': coords[1],
                    'place_name': feature['place_name']
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur géocodage: {e}")
            return None
    
    def get_map_url(self, longitude: float, latitude: float, 
                   zoom: int = 15, width: int = 600, height: int = 400) -> Optional[str]:
        """
        Génère une URL de carte statique
        
        Args:
            longitude: Longitude
            latitude: Latitude
            zoom: Niveau de zoom
            width: Largeur en pixels
            height: Hauteur en pixels
        
        Returns:
            URL de la carte
        """
        if not self.enabled:
            return None
        
        return (f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"
                f"{longitude},{latitude},{zoom}/{width}x{height}"
                f"?access_token={self.access_token}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut de Mapbox"""
        return {
            'enabled': self.enabled,
            'free_tier_limit': '50000 requêtes/mois'
        }


mapbox_service = MapboxService()
