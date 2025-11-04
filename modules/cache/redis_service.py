"""
Service de cache Redis
Optimisé pour le free tier avec stratégies intelligentes
"""
import logging
from typing import Optional, Any, Dict
import json
from datetime import timedelta

logger = logging.getLogger(__name__)


class RedisService:
    """
    Gestion du cache Redis
    - Cache intelligent avec TTL
    - Optimisation mémoire (30MB limit free tier)
    - Stratégies d'éviction
    """
    
    def __init__(self):
        self.client = None
        self.enabled = False
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialise la connexion Redis"""
        try:
            import redis
            from config.settings import Config
            
            keys = Config.get_api_keys()
            redis_url = keys['redis']['url']
            
            if redis_url:
                self.client = redis.from_url(redis_url, decode_responses=True)
                self.client.ping()
                self.enabled = True
                logger.info("✓ Redis connecté")
            else:
                logger.warning("✗ Redis URL manquante")
                
        except ImportError:
            logger.error("Module redis non installé")
        except Exception as e:
            logger.error(f"Erreur connexion Redis: {e}")
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        Stocke une valeur dans le cache
        
        Args:
            key: Clé
            value: Valeur (sera sérialisée en JSON)
            ttl: Durée de vie en secondes (défaut: 1h)
        
        Returns:
            True si succès, False sinon
        """
        if not self.enabled:
            return False
        
        try:
            serialized = json.dumps(value)
            self.client.setex(key, ttl, serialized)
            logger.debug(f"✓ Cache set: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur cache set: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Récupère une valeur du cache
        
        Args:
            key: Clé
        
        Returns:
            Valeur désérialisée ou None si non trouvée
        """
        if not self.enabled:
            return None
        
        try:
            value = self.client.get(key)
            if value:
                logger.debug(f"✓ Cache hit: {key}")
                return json.loads(value)
            else:
                logger.debug(f"✗ Cache miss: {key}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur cache get: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """Supprime une clé du cache"""
        if not self.enabled:
            return False
        
        try:
            self.client.delete(key)
            logger.debug(f"✓ Cache delete: {key}")
            return True
        except Exception as e:
            logger.error(f"Erreur cache delete: {e}")
            return False
    
    def clear_all(self) -> bool:
        """Vide tout le cache (à utiliser avec précaution)"""
        if not self.enabled:
            return False
        
        try:
            self.client.flushdb()
            logger.warning("⚠ Cache entièrement vidé")
            return True
        except Exception as e:
            logger.error(f"Erreur clear cache: {e}")
            return False
    
    def get_stats(self) -> Optional[Dict[str, Any]]:
        """Retourne les statistiques du cache"""
        if not self.enabled:
            return None
        
        try:
            info = self.client.info('memory')
            return {
                'used_memory': info.get('used_memory_human'),
                'used_memory_peak': info.get('used_memory_peak_human'),
                'total_keys': self.client.dbsize()
            }
        except Exception as e:
            logger.error(f"Erreur stats Redis: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du module Redis"""
        status = {
            'enabled': self.enabled,
            'connected': False
        }
        
        if self.enabled and self.client:
            try:
                self.client.ping()
                status['connected'] = True
                status['stats'] = self.get_stats()
            except:
                pass
        
        return status


redis_service = RedisService()
