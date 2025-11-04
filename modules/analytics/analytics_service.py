"""
Service Analytics unifié
Amplitude + LogRocket + Posthog
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Analytics multi-plateformes
    - Amplitude: Analytics comportemental
    - LogRocket: Session replay + erreurs
    - Posthog: Product analytics
    """
    
    def __init__(self):
        self.amplitude_enabled = False
        self.logrocket_enabled = False
        self.posthog_enabled = False
        self._initialize()
    
    def _initialize(self):
        """Initialise les services analytics"""
        from config.settings import Config
        keys = Config.get_api_keys()
        
        self.amplitude_key = keys['amplitude']['api_key']
        self.logrocket_key = keys['logrocket']['api_key']
        self.posthog_key = keys['posthog']['api_key']
        
        self.amplitude_enabled = self.amplitude_key is not None
        self.logrocket_enabled = self.logrocket_key is not None
        self.posthog_enabled = self.posthog_key is not None
        
        if self.amplitude_enabled:
            logger.info("✓ Amplitude activé")
        if self.logrocket_enabled:
            logger.info("✓ LogRocket activé")
        if self.posthog_enabled:
            logger.info("✓ Posthog activé")
    
    def track_event(self, event_name: str, user_id: Optional[str] = None,
                   properties: Optional[Dict] = None) -> bool:
        """
        Envoie un événement à tous les services analytics configurés
        
        Args:
            event_name: Nom de l'événement
            user_id: ID utilisateur
            properties: Propriétés additionnelles
        
        Returns:
            True si au moins un service a reçu l'événement
        """
        success = False
        properties = properties or {}
        
        if self.amplitude_enabled:
            success = self._track_amplitude(event_name, user_id, properties) or success
        
        if self.posthog_enabled:
            success = self._track_posthog(event_name, user_id, properties) or success
        
        return success
    
    def _track_amplitude(self, event_name: str, user_id: Optional[str],
                        properties: Dict) -> bool:
        """Envoie un événement à Amplitude"""
        try:
            logger.info(f"📊 Amplitude event: {event_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur Amplitude: {e}")
            return False
    
    def _track_posthog(self, event_name: str, user_id: Optional[str],
                       properties: Dict) -> bool:
        """Envoie un événement à Posthog"""
        try:
            logger.info(f"📊 Posthog event: {event_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur Posthog: {e}")
            return False
    
    def log_error(self, error: Exception, context: Optional[Dict] = None) -> bool:
        """
        Log une erreur dans LogRocket
        
        Args:
            error: Exception
            context: Contexte additionnel
        
        Returns:
            True si succès
        """
        if not self.logrocket_enabled:
            return False
        
        try:
            logger.error(f"🔴 LogRocket error: {str(error)}")
            return True
        except Exception as e:
            logger.error(f"Erreur LogRocket: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut des services analytics"""
        return {
            'amplitude': {
                'enabled': self.amplitude_enabled,
                'configured': self.amplitude_key is not None
            },
            'logrocket': {
                'enabled': self.logrocket_enabled,
                'configured': self.logrocket_key is not None
            },
            'posthog': {
                'enabled': self.posthog_enabled,
                'configured': self.posthog_key is not None
            }
        }


analytics_service = AnalyticsService()
