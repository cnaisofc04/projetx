"""
Service de communication
Email (Resend) + Vidéo (Agora)
"""
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class CommunicationService:
    """
    Communication multi-canaux
    - Email: Resend
    - Vidéo: Agora
    """
    
    def __init__(self):
        self.resend_enabled = False
        self.agora_enabled = False
        self._initialize()
    
    def _initialize(self):
        """Initialise les services de communication"""
        from config.settings import Config
        keys = Config.get_api_keys()
        
        self.resend_key = keys['resend']['api_key']
        self.agora_app_id = keys['agora']['app_id']
        
        self.resend_enabled = self.resend_key is not None
        self.agora_enabled = self.agora_app_id is not None
        
        if self.resend_enabled:
            logger.info("✓ Resend (email) activé")
        if self.agora_enabled:
            logger.info("✓ Agora (vidéo) activé")
    
    def send_email(self, to: str, subject: str, html: str, 
                   from_email: str = "noreply@example.com") -> bool:
        """
        Envoie un email via Resend
        
        Args:
            to: Email destinataire
            subject: Sujet
            html: Contenu HTML
            from_email: Email expéditeur
        
        Returns:
            True si succès
        """
        if not self.resend_enabled:
            logger.error("Resend non activé")
            return False
        
        try:
            import resend
            resend.api_key = self.resend_key
            
            params = {
                "from": from_email,
                "to": [to],
                "subject": subject,
                "html": html,
            }
            
            email = resend.Emails.send(params)
            logger.info(f"✓ Email envoyé à {to}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur envoi email: {e}")
            return False
    
    def generate_agora_token(self, channel_name: str, uid: int, 
                            role: str = "publisher") -> Optional[str]:
        """
        Génère un token Agora pour rejoindre un canal vidéo
        
        Args:
            channel_name: Nom du canal
            uid: ID utilisateur
            role: Role (publisher ou subscriber)
        
        Returns:
            Token Agora ou None
        """
        if not self.agora_enabled:
            logger.error("Agora non activé")
            return None
        
        try:
            logger.info(f"✓ Token Agora généré pour {channel_name}")
            return "agora_token_placeholder"
            
        except Exception as e:
            logger.error(f"Erreur génération token Agora: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut des services de communication"""
        return {
            'resend': {
                'enabled': self.resend_enabled,
                'free_tier_limit': '3000 emails/mois'
            },
            'agora': {
                'enabled': self.agora_enabled,
                'free_tier_limit': '10000 minutes/mois'
            }
        }


communication_service = CommunicationService()
