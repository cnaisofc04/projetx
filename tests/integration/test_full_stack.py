"""
Tests d'intégration - Vérifie que tous les modules fonctionnent ensemble
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def test_all_modules_initialization():
    """Vérifie que tous les modules s'initialisent correctement"""
    from modules.auth.auth_service import auth_service
    from modules.payments.stripe_service import stripe_service
    from modules.cache.redis_service import redis_service
    from modules.ai.openai_service import openai_service
    from modules.analytics.analytics_service import analytics_service
    from modules.communication.communication_service import communication_service
    from modules.collaboration.collaboration_service import collaboration_service
    from modules.geolocation.mapbox_service import mapbox_service
    from modules.services.additional_services import additional_services
    
    modules = [
        ('Auth', auth_service),
        ('Payments', stripe_service),
        ('Cache', redis_service),
        ('AI', openai_service),
        ('Analytics', analytics_service),
        ('Communication', communication_service),
        ('Collaboration', collaboration_service),
        ('Geolocation', mapbox_service),
        ('Services', additional_services),
    ]
    
    for name, service in modules:
        status = service.get_status()
        assert status is not None, f"{name} status should not be None"
        print(f"✓ {name} initialisé correctement")


def test_flask_app_integration():
    """Vérifie que l'application Flask intègre tous les modules"""
    from app import app
    
    assert app is not None
    assert app.config['SQLALCHEMY_DATABASE_URI'] is not None
    
    print("✓ Application Flask intégrée correctement")


def test_dashboard_routes():
    """Vérifie que les routes du dashboard fonctionnent"""
    from app import app
    
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        print("✓ Dashboard route: OK")
        
        response = client.get('/api/status')
        assert response.status_code == 200
        data = response.get_json()
        assert 'modules' in data
        assert 'timestamp' in data
        print("✓ API Status route: OK")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
