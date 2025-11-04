"""
Module de paiements Stripe
- Intégration Stripe SDK
- Webhooks sécurisés
- Mode test/sandbox
"""

from .stripe_service import StripeService

__all__ = ['StripeService']
