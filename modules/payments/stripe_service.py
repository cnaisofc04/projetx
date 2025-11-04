"""
Service de paiements Stripe
Gestion complète des paiements, abonnements et webhooks
"""
import logging
from typing import Optional, Dict, Any
from security.api_manager import api_key_manager

logger = logging.getLogger(__name__)


class StripeService:
    """
    Intégration Stripe complète
    - Paiements one-time
    - Abonnements récurrents
    - Webhooks sécurisés
    - Mode test/production
    """
    
    def __init__(self):
        self.stripe = None
        self.public_key = None
        self.secret_key = None
        self.enabled = False
        self._initialize_stripe()
    
    def _initialize_stripe(self):
        """Initialise Stripe avec les clés API"""
        try:
            import stripe
            from config.settings import Config
            
            keys = Config.get_api_keys()
            self.public_key = keys['stripe']['public']
            self.secret_key = keys['stripe']['secret']
            
            if self.secret_key:
                stripe.api_key = self.secret_key
                self.stripe = stripe
                self.enabled = True
                logger.info("✓ Stripe initialisé (mode sandbox)")
            else:
                logger.warning("✗ Clés Stripe manquantes")
                
        except ImportError:
            logger.error("Module stripe non installé")
        except Exception as e:
            logger.error(f"Erreur initialisation Stripe: {e}")
    
    def create_payment_intent(self, amount: int, currency: str = 'eur', 
                             metadata: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Crée un PaymentIntent Stripe
        
        Args:
            amount: Montant en centimes (ex: 1000 = 10.00 EUR)
            currency: Devise (eur, usd, etc.)
            metadata: Métadonnées additionnelles
        
        Returns:
            PaymentIntent créé ou None si erreur
        """
        if not self.enabled:
            logger.error("Stripe non activé")
            return None
        
        try:
            intent = self.stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata or {},
            )
            
            logger.info(f"✓ PaymentIntent créé: {intent.id}")
            
            return {
                'id': intent.id,
                'client_secret': intent.client_secret,
                'amount': intent.amount,
                'currency': intent.currency,
                'status': intent.status
            }
            
        except Exception as e:
            logger.error(f"Erreur création PaymentIntent: {e}")
            return None
    
    def create_subscription(self, customer_id: str, price_id: str) -> Optional[Dict[str, Any]]:
        """
        Crée un abonnement Stripe
        
        Args:
            customer_id: ID du client Stripe
            price_id: ID du prix/plan
        
        Returns:
            Abonnement créé ou None si erreur
        """
        if not self.enabled:
            logger.error("Stripe non activé")
            return None
        
        try:
            subscription = self.stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
            )
            
            logger.info(f"✓ Abonnement créé: {subscription.id}")
            
            return {
                'id': subscription.id,
                'status': subscription.status,
                'current_period_end': subscription.current_period_end
            }
            
        except Exception as e:
            logger.error(f"Erreur création abonnement: {e}")
            return None
    
    def verify_webhook_signature(self, payload: bytes, signature: str, 
                                 webhook_secret: str) -> Optional[Any]:
        """
        Vérifie la signature d'un webhook Stripe
        
        Args:
            payload: Corps de la requête
            signature: Signature Stripe
            webhook_secret: Secret du webhook
        
        Returns:
            Event Stripe si valide, None sinon
        """
        if not self.enabled:
            return None
        
        try:
            event = self.stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            logger.info(f"✓ Webhook vérifié: {event.type}")
            return event
            
        except Exception as e:
            logger.error(f"Erreur vérification webhook: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du module Stripe"""
        return {
            'enabled': self.enabled,
            'public_key_configured': self.public_key is not None,
            'secret_key_configured': self.secret_key is not None,
            'mode': 'test' if self.secret_key and 'sk_test' in self.secret_key else 'live'
        }


stripe_service = StripeService()
