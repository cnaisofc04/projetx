
"""
Gestionnaire centralisé et sécurisé des API keys - ULTRA MODULAIRE
Chaque plateforme est gérée indépendamment avec toutes ses fonctions
"""
import os
import logging
from typing import Optional, Dict, Any, List
from functools import lru_cache

logger = logging.getLogger(__name__)


class APIKeyManager:
    """
    Gestionnaire sécurisé ultra-modulaire des clés API
    - Toutes les plateformes supportées
    - Toutes les clés reconnues
    - Validation complète par plateforme
    """
    
    # Mapping COMPLET de toutes les plateformes
    PLATFORMS = {
        # Authentication & Backend
        'supabase': {
            'keys': ['URL_SUPABASE_AUTOQG', 'SUPABASE_ANON_PUBLIC', 'SUPABASE_AUTOQG_API_KEY', 
                    'SUPABASE_ROLE_SECRET', 'api_key_secret_supabase'],
            'name': 'Supabase',
            'type': 'backend'
        },
        'appwrite': {
            'keys': ['API_ENDPOINT_APPRWRITE', 'PROJET_ID_APPWRITE'],
            'name': 'Appwrite',
            'type': 'backend'
        },
        
        # Payments
        'stripe': {
            'keys': ['STRIPE_API_KEY_SECRET', 'STRIPE_API_KEY_PUBLIC'],
            'name': 'Stripe',
            'type': 'payment'
        },
        
        # AI & Machine Learning
        'openai': {
            'keys': ['OPEN_AI_API_KEY', 'MY_TEST_KEY_OPEN_AI_API'],
            'name': 'OpenAI',
            'type': 'ai'
        },
        
        # Cache & Database
        'redis': {
            'keys': ['REDIS_API_KEY', 'REDIS_URL_us_east_1', 'REDIS_API_account_key',
                    'REDIS_CLI', 'REDIS_API_KEY_GENERATED_LangCache', 'REDIS_CACHE_ID',
                    'REDIS_CLIENT', 'REDIS_SERVICE_NAME', 'REDIS_QUICK_CONNECT'],
            'name': 'Redis',
            'type': 'cache'
        },
        'postgres': {
            'keys': ['DATABASE_URL', 'PGDATABASE', 'PGHOST', 'PGPORT', 'PGUSER', 'PGPASSWORD'],
            'name': 'PostgreSQL',
            'type': 'database'
        },
        
        # Version Control & Collaboration
        'github': {
            'keys': ['GITHUB_TOKEN_API'],
            'name': 'GitHub',
            'type': 'collaboration'
        },
        'gitlab': {
            'keys': ['TOKEN_API_GITLAB'],
            'name': 'GitLab',
            'type': 'collaboration'
        },
        'trello': {
            'keys': ['TRELLO_API_KEY', 'TRELLO_TOKEN'],
            'name': 'Trello',
            'type': 'collaboration'
        },
        
        # Communication
        'resend': {
            'keys': ['RESEND_API_KEY'],
            'name': 'Resend',
            'type': 'communication'
        },
        'agora': {
            'keys': ['AGORA_APP_ID', 'AGORA_Primary_Certificate', 'AGORA_Secondary_Certificate'],
            'name': 'Agora',
            'type': 'communication'
        },
        
        # Analytics & Monitoring
        'amplitude': {
            'keys': ['AMPLITUDE_API_KEY', 'AMPLITUDE_Standard_Server_url', 'AMPLITUDE_EU_Residency_Server_URL'],
            'name': 'Amplitude',
            'type': 'analytics'
        },
        'logrocket': {
            'keys': ['LOG_ROCKET_API_KEY', 'LOG_ROCKET_App_ID', 'LOG_ROCKET_Project_Name',
                    'LOG_ROCKET_Manually_sanitize_text_and_inputs',
                    'LOG_ROCKET_Automatically_sanitize_all_text_and_inputs',
                    'LOG_ROCKET_Automatically_sanitize_all_text_and_inputs_2',
                    'LOG_ROCKET_Automatically_sanitize_network_requests',
                    'LOG_ROCKET_Automatically_sanitize_network_responses'],
            'name': 'LogRocket',
            'type': 'analytics'
        },
        'posthog': {
            'keys': ['POSTHOG_API_KEY'],
            'name': 'PostHog',
            'type': 'analytics'
        },
        
        # Maps & Location
        'mapbox': {
            'keys': ['MAPBOX_ACCESS_TOKEN'],
            'name': 'Mapbox',
            'type': 'geolocation'
        },
        
        # Data & Storage
        'airtable': {
            'keys': ['AIRTABLE_API_KEY'],
            'name': 'Airtable',
            'type': 'data'
        },
        
        # Automation & Workflows
        'pipedream': {
            'keys': ['PIPEDREAM_API_KEY_Client_ID', 'PIPEDREAM_API_KEY_Client_Secret', 
                    'PIPEDREAM_Workspace_ID'],
            'name': 'Pipedream',
            'type': 'automation'
        },
        
        # Mobile Development
        'expo': {
            'keys': ['EXPO_API_KEY'],
            'name': 'Expo',
            'type': 'mobile'
        },
        
        # AI Assistants
        'flowith': {
            'keys': ['FLOWITH_API_KEY'],
            'name': 'Flowith',
            'type': 'ai'
        },
        
        # Custom APIs
        'gabriel': {
            'keys': ['GABRIEL_API_KEY_1'],
            'name': 'Gabriel API',
            'type': 'custom'
        },
        'manus': {
            'keys': ['MANUS_API_KEY'],
            'name': 'Manus API',
            'type': 'custom'
        },
        
        # Testing
        'test_node': {
            'keys': ['Try_out_Your_new_API_key_NODE'],
            'name': 'Test Node API',
            'type': 'test'
        },
        'test_python': {
            'keys': ['Try_out_your_new_API_key_Python'],
            'name': 'Test Python API',
            'type': 'test'
        },
        
        # Security
        'session': {
            'keys': ['SESSION_SECRET'],
            'name': 'Session',
            'type': 'security'
        }
    }
    
    def __init__(self):
        self._platform_status = {}
        self._key_values = {}
        self._check_all_platforms()
    
    def _check_all_platforms(self):
        """Vérifie TOUTES les plateformes et TOUTES leurs clés"""
        logger.info("="*60)
        logger.info("🔍 VÉRIFICATION COMPLÈTE DE TOUTES LES PLATEFORMES")
        logger.info("="*60)
        
        for platform_id, platform_info in self.PLATFORMS.items():
            platform_name = platform_info['name']
            platform_type = platform_info['type']
            keys = platform_info['keys']
            
            # Vérifier chaque clé de la plateforme
            available_keys = []
            missing_keys = []
            
            for key in keys:
                value = os.environ.get(key)
                if value and len(value) > 0:
                    available_keys.append(key)
                    self._key_values[key] = value
                else:
                    missing_keys.append(key)
            
            # Déterminer le statut de la plateforme
            if len(available_keys) == len(keys):
                status = 'COMPLET'
                symbol = '✅'
            elif len(available_keys) > 0:
                status = 'PARTIEL'
                symbol = '⚠️'
            else:
                status = 'MANQUANT'
                symbol = '❌'
            
            self._platform_status[platform_id] = {
                'name': platform_name,
                'type': platform_type,
                'status': status,
                'available_keys': available_keys,
                'missing_keys': missing_keys,
                'total_keys': len(keys),
                'available_count': len(available_keys)
            }
            
            logger.info(f"{symbol} {platform_name} ({platform_type}): {status} - "
                       f"{len(available_keys)}/{len(keys)} clés")
            
            if missing_keys:
                logger.warning(f"   Clés manquantes: {', '.join(missing_keys)}")
    
    @lru_cache(maxsize=256)
    def get_key(self, platform: str, key_name: Optional[str] = None) -> Optional[str]:
        """
        Récupère une clé API de manière sécurisée
        
        Args:
            platform: ID de la plateforme (ex: 'openai', 'stripe')
            key_name: Nom spécifique de la clé (optionnel)
        
        Returns:
            La clé API ou None si non disponible
        """
        if platform not in self.PLATFORMS:
            logger.error(f"❌ Plateforme inconnue: {platform}")
            return None
        
        platform_info = self.PLATFORMS[platform]
        keys = platform_info['keys']
        
        if key_name:
            # Recherche d'une clé spécifique
            if key_name in self._key_values:
                return self._key_values[key_name]
            logger.error(f"❌ Clé {key_name} non trouvée pour {platform}")
            return None
        else:
            # Retourne la première clé disponible
            for key in keys:
                if key in self._key_values:
                    return self._key_values[key]
            logger.error(f"❌ Aucune clé disponible pour {platform}")
            return None
    
    def get_all_keys(self, platform: str) -> Dict[str, str]:
        """Retourne toutes les clés disponibles pour une plateforme"""
        if platform not in self.PLATFORMS:
            return {}
        
        result = {}
        for key in self.PLATFORMS[platform]['keys']:
            if key in self._key_values:
                result[key] = self._key_values[key]
        
        return result
    
    def is_platform_available(self, platform: str, require_complete: bool = False) -> bool:
        """
        Vérifie si une plateforme est disponible
        
        Args:
            platform: ID de la plateforme
            require_complete: Si True, nécessite que TOUTES les clés soient présentes
        
        Returns:
            True si la plateforme est disponible
        """
        if platform not in self._platform_status:
            return False
        
        status = self._platform_status[platform]['status']
        
        if require_complete:
            return status == 'COMPLET'
        else:
            return status in ['COMPLET', 'PARTIEL']
    
    def get_platform_status(self, platform: str) -> Dict[str, Any]:
        """Retourne le statut détaillé d'une plateforme"""
        return self._platform_status.get(platform, {})
    
    def get_all_platforms_status(self) -> Dict[str, Dict[str, Any]]:
        """Retourne le statut de toutes les plateformes"""
        return self._platform_status.copy()
    
    def get_platforms_by_type(self, platform_type: str) -> List[str]:
        """Retourne la liste des plateformes d'un type donné"""
        return [
            platform_id 
            for platform_id, info in self.PLATFORMS.items() 
            if info['type'] == platform_type
        ]
    
    def get_summary(self) -> Dict[str, Any]:
        """Génère un résumé complet de l'état des plateformes"""
        total_platforms = len(self.PLATFORMS)
        complete = sum(1 for p in self._platform_status.values() if p['status'] == 'COMPLET')
        partial = sum(1 for p in self._platform_status.values() if p['status'] == 'PARTIEL')
        missing = sum(1 for p in self._platform_status.values() if p['status'] == 'MANQUANT')
        
        total_keys = sum(p['total_keys'] for p in self._platform_status.values())
        available_keys = sum(p['available_count'] for p in self._platform_status.values())
        
        return {
            'total_platforms': total_platforms,
            'complete': complete,
            'partial': partial,
            'missing': missing,
            'total_keys': total_keys,
            'available_keys': available_keys,
            'completion_rate': (available_keys / total_keys * 100) if total_keys > 0 else 0
        }


# Instance globale
api_key_manager = APIKeyManager()
