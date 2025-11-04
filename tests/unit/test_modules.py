"""
Tests unitaires pour tous les modules
Chaque module est testé indépendamment
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def test_auth_module():
    """Test du module d'authentification"""
    from modules.auth.auth_service import auth_service
    
    status = auth_service.get_status()
    assert 'enabled' in status
    assert 'jwt_enabled' in status
    print("✓ Module Auth: OK")


def test_payments_module():
    """Test du module de paiements"""
    from modules.payments.stripe_service import stripe_service
    
    status = stripe_service.get_status()
    assert 'enabled' in status
    assert 'mode' in status
    print("✓ Module Payments: OK")


def test_cache_module():
    """Test du module de cache"""
    from modules.cache.redis_service import redis_service
    
    status = redis_service.get_status()
    assert 'enabled' in status
    print("✓ Module Cache: OK")


def test_ai_module():
    """Test du module IA"""
    from modules.ai.openai_service import openai_service
    
    status = openai_service.get_status()
    assert 'enabled' in status
    print("✓ Module IA: OK")


def test_analytics_module():
    """Test du module analytics"""
    from modules.analytics.analytics_service import analytics_service
    
    status = analytics_service.get_status()
    assert 'amplitude' in status
    assert 'logrocket' in status
    assert 'posthog' in status
    print("✓ Module Analytics: OK")


def test_communication_module():
    """Test du module communication"""
    from modules.communication.communication_service import communication_service
    
    status = communication_service.get_status()
    assert 'resend' in status
    assert 'agora' in status
    print("✓ Module Communication: OK")


def test_collaboration_module():
    """Test du module collaboration"""
    from modules.collaboration.collaboration_service import collaboration_service
    
    status = collaboration_service.get_status()
    assert 'github' in status
    assert 'gitlab' in status
    assert 'trello' in status
    print("✓ Module Collaboration: OK")


def test_geolocation_module():
    """Test du module géolocalisation"""
    from modules.geolocation.mapbox_service import mapbox_service
    
    status = mapbox_service.get_status()
    assert 'enabled' in status
    print("✓ Module Géolocalisation: OK")


def test_additional_services_module():
    """Test des services additionnels"""
    from modules.services.additional_services import additional_services
    
    status = additional_services.get_status()
    assert 'appwrite' in status
    assert 'airtable' in status
    print("✓ Module Services Additionnels: OK")


def test_security_api_manager():
    """Test du gestionnaire de sécurité API"""
    from security.api_manager import api_key_manager
    
    status = api_key_manager.get_status()
    assert isinstance(status, dict)
    print("✓ Security API Manager: OK")


def test_config_settings():
    """Test de la configuration"""
    from config.settings import Config
    
    api_keys = Config.get_api_keys()
    assert isinstance(api_keys, dict)
    assert 'openai' in api_keys
    assert 'stripe' in api_keys
    print("✓ Configuration: OK")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
