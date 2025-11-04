"""
Gestionnaire centralisé et sécurisé des API keys
Principe: Aucune clé n'est jamais exposée en clair dans le code
"""
import os
import logging
from typing import Optional, Dict, Any
from functools import lru_cache

logger = logging.getLogger(__name__)


class APIKeyManager:
    """
    Gestionnaire sécurisé des clés API
    - Charge les clés depuis l'environnement
    - Vérifie leur présence
    - Ne log jamais les valeurs réelles
    - Cache les résultats pour performance
    """
    
    def __init__(self):
        self._available_keys = {}
        self._check_all_keys()
    
    def _check_all_keys(self):
        """Vérifie quelles clés API sont disponibles sans les exposer"""
        all_env_keys = [
            'OPEN_AI_API_KEY', 'STRIPE_API_KEY_SECRET', 'STRIPE_API_KEY_PUBLIC',
            'SUPABASE_AUTOQG_API_KEY', 'REDIS_API_KEY', 'GITHUB_TOKEN_API',
            'GITLAB_TOKEN', 'TRELLO_API_KEY', 'RESEND_API_KEY', 
            'AMPLITUDE_API_KEY', 'LOG_ROCKET_API_KEY', 'AGORA_APP_ID',
            'MAPBOX_ACCESS_TOKEN', 'AIRTABLE_API_KEY', 'POSTHOG_API_KEY',
        ]
        
        for key in all_env_keys:
            value = os.environ.get(key)
            self._available_keys[key] = value is not None and len(value) > 0
            
            if self._available_keys[key]:
                logger.info(f"✓ {key} disponible")
            else:
                logger.warning(f"✗ {key} manquante")
    
    @lru_cache(maxsize=128)
    def get_key(self, service: str, key_name: str = 'api_key') -> Optional[str]:
        """
        Récupère une clé API de manière sécurisée
        
        Args:
            service: Nom du service (ex: 'openai', 'stripe')
            key_name: Nom spécifique de la clé (ex: 'secret', 'public')
        
        Returns:
            La clé API ou None si non disponible
        """
        env_var_map = {
            'openai': 'OPEN_AI_API_KEY',
            'stripe_secret': 'STRIPE_API_KEY_SECRET',
            'stripe_public': 'STRIPE_API_KEY_PUBLIC',
            'supabase': 'SUPABASE_AUTOQG_API_KEY',
            'redis': 'REDIS_API_KEY',
            'github': 'GITHUB_TOKEN_API',
            'gitlab': 'TOKEN_API_GITLAB',
            'trello': 'TRELLO_API_KEY',
            'resend': 'RESEND_API_KEY',
            'amplitude': 'AMPLITUDE_API_KEY',
            'logrocket': 'LOG_ROCKET_API_KEY',
            'agora': 'AGORA_APP_ID',
            'mapbox': 'MAPBOX_ACCESS_TOKEN',
            'airtable': 'AIRTABLE_API_KEY',
            'posthog': 'POSTHOG_API_KEY',
        }
        
        env_var = env_var_map.get(service)
        if not env_var:
            logger.error(f"Service inconnu: {service}")
            return None
        
        value = os.environ.get(env_var)
        if not value:
            logger.error(f"Clé API manquante pour {service}")
            return None
        
        return value
    
    def is_available(self, service: str) -> bool:
        """Vérifie si une clé API est disponible"""
        key = self.get_key(service)
        return key is not None and len(key) > 0
    
    def get_status(self) -> Dict[str, bool]:
        """Retourne le statut de toutes les clés (disponible ou non)"""
        return self._available_keys.copy()


api_key_manager = APIKeyManager()
