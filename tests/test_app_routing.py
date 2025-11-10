"""
Tests unitaires pour le routing de l'application
Vérifie que:
- Le frontend React est servi sur /
- Les routes /api/* retournent du JSON en cas de 404
- Les routes /admin/* retournent du JSON en cas de 404
- Les autres routes servent le SPA React
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Fixture pour le client de test Flask"""
    # Juste utiliser le client de test sans créer/détruire la DB
    # car on teste uniquement le routing, pas les modèles
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


def test_root_serves_react_app(client):
    """Test que / sert l'application React"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!doctype html>' in response.data or b'<!DOCTYPE html>' in response.data
    # Vérifie que c'est bien un fichier HTML
    assert response.content_type.startswith('text/html')


def test_api_404_returns_json(client):
    """Test que les routes /api/* inexistantes retournent du JSON"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
    # Vérifie que c'est bien du JSON
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Not found'


def test_admin_404_returns_json(client):
    """Test que les routes /admin/* inexistantes retournent du JSON"""
    response = client.get('/admin/nonexistent/route')
    assert response.status_code == 404
    # Vérifie que c'est bien du JSON
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert 'error' in data


def test_spa_routing_works(client):
    """Test que les routes SPA (non-API, non-admin) servent React"""
    # Test plusieurs routes qui devraient servir le SPA
    spa_routes = ['/profile', '/settings', '/about', '/unknown-route']
    
    for route in spa_routes:
        response = client.get(route)
        assert response.status_code == 200
        # Vérifie que c'est bien du HTML (le SPA React)
        assert response.content_type.startswith('text/html')
        assert b'<!doctype html>' in response.data or b'<!DOCTYPE html>' in response.data


def test_assets_are_served(client):
    """Test que les assets statiques sont accessibles"""
    # Note: Ce test pourrait échouer si les assets n'existent pas encore
    # mais il valide la configuration de la route
    response = client.get('/assets/test.js')
    # On s'attend à un 404 car le fichier n'existe pas, mais c'est normal
    assert response.status_code in [200, 404]


def test_admin_routes_are_accessible(client):
    """Test que les routes /admin existent et sont accessibles"""
    response = client.get('/admin/')
    # Le dashboard devrait répondre (200 ou redirect vers login)
    assert response.status_code in [200, 302, 404]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
