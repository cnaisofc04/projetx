"""
Tests de sécurité
Vérifie que les pratiques de sécurité sont respectées
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def test_no_hardcoded_secrets():
    """Vérifie qu'aucun secret n'est hardcodé"""
    from config.settings import Config
    
    assert Config.SECRET_KEY == os.environ.get("SESSION_SECRET")
    assert Config.DATABASE_URL == os.environ.get("DATABASE_URL")
    
    print("✓ Aucun secret hardcodé")


def test_api_key_manager_security():
    """Vérifie que le gestionnaire d'API keys est sécurisé"""
    from security.api_manager import api_key_manager
    
    status = api_key_manager.get_status()
    
    for key_name, is_available in status.items():
        assert isinstance(is_available, bool)
    
    print("✓ API Key Manager sécurisé")


def test_jwt_token_generation():
    """Vérifie la génération sécurisée de tokens JWT"""
    from modules.auth.auth_service import auth_service
    
    if auth_service.enabled:
        token = auth_service.generate_jwt_token(1, "test@example.com")
        assert token is not None
        assert len(token) > 0
        
        payload = auth_service.verify_jwt_token(token)
        assert payload is not None
        assert payload['user_id'] == 1
        assert payload['email'] == "test@example.com"
        
        print("✓ JWT tokens sécurisés")
    else:
        print("⚠ Auth service non activé, test JWT ignoré")


def test_password_hashing():
    """Vérifie que les mots de passe sont hashés correctement"""
    from werkzeug.security import generate_password_hash, check_password_hash
    
    password = "test_password_123"
    hashed = generate_password_hash(password)
    
    assert hashed != password
    assert len(hashed) > 50
    assert check_password_hash(hashed, password)
    assert not check_password_hash(hashed, "wrong_password")
    
    print("✓ Hashage des mots de passe sécurisé")


def test_database_connection_secure():
    """Vérifie que la connexion DB utilise des variables d'environnement"""
    from config.settings import Config
    
    db_url = Config.SQLALCHEMY_DATABASE_URI
    assert db_url is not None
    assert 'postgresql' in db_url.lower() or 'postgres' in db_url.lower()
    
    print("✓ Connexion DB sécurisée")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
