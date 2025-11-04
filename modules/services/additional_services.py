"""
Services additionnels
Appwrite, Airtable, etc.
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class AdditionalServices:
    """
    Services additionnels
    - Appwrite: Backend as a Service
    - Airtable: Base de données collaborative
    """
    
    def __init__(self):
        self.appwrite_enabled = False
        self.airtable_enabled = False
        self._initialize()
    
    def _initialize(self):
        """Initialise les services additionnels"""
        from config.settings import Config
        keys = Config.get_api_keys()
        
        self.appwrite_endpoint = keys['appwrite']['endpoint']
        self.appwrite_project_id = keys['appwrite']['project_id']
        self.airtable_key = keys['airtable']['api_key']
        
        self.appwrite_enabled = (self.appwrite_endpoint is not None and 
                                 self.appwrite_project_id is not None)
        self.airtable_enabled = self.airtable_key is not None
        
        if self.appwrite_enabled:
            logger.info("✓ Appwrite activé")
        if self.airtable_enabled:
            logger.info("✓ Airtable activé")
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut des services additionnels"""
        return {
            'appwrite': {
                'enabled': self.appwrite_enabled,
                'features': ['Database', 'Auth', 'Storage', 'Functions']
            },
            'airtable': {
                'enabled': self.airtable_enabled,
                'free_tier_limit': '1000 enregistrements/base'
            }
        }


additional_services = AdditionalServices()
