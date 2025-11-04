"""
Service d'authentification centralisé
Utilise Supabase Auth + JWT pour une authentification sécurisée
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from security.api_manager import api_key_manager

logger = logging.getLogger(__name__)


class AuthService:
    """
    Gestion de l'authentification avec Supabase et JWT
    - Inscription/Connexion
    - Génération de tokens
    - Vérification des sessions
    """
    
    def __init__(self):
        self.supabase_url = None
        self.supabase_key = None
        self._initialize_supabase()
    
    def _initialize_supabase(self):
        """Initialise la connexion Supabase si disponible"""
        try:
            from config.settings import Config
            keys = Config.get_api_keys()
            
            self.supabase_url = keys['supabase']['url']
            self.supabase_key = keys['supabase']['api_key']
            
            if self.supabase_url and self.supabase_key:
                logger.info("✓ Supabase Auth initialisé")
                self.enabled = True
            else:
                logger.warning("✗ Supabase Auth non configuré")
                self.enabled = False
                
        except Exception as e:
            logger.error(f"Erreur initialisation Supabase: {e}")
            self.enabled = False
    
    def generate_jwt_token(self, user_id: int, email: str, expires_in_hours: int = 24) -> str:
        """
        Génère un JWT token pour un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            email: Email de l'utilisateur
            expires_in_hours: Durée de validité en heures
        
        Returns:
            JWT token signé
        """
        from config.settings import Config
        
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
            'iat': datetime.utcnow(),
        }
        
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
        return token
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Vérifie et décode un JWT token
        
        Args:
            token: JWT token à vérifier
        
        Returns:
            Payload du token si valide, None sinon
        """
        from config.settings import Config
        
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expiré")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Token invalide")
            return None
    
    def create_user(self, email: str, password: str, username: str) -> Optional[Dict[str, Any]]:
        """
        Crée un nouvel utilisateur
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe
            username: Nom d'utilisateur
        
        Returns:
            Données utilisateur si succès, None sinon
        """
        try:
            from models import User
            from app import db
            from werkzeug.security import generate_password_hash
            
            existing_user = User.query.filter(
                (User.email == email) | (User.username == username)
            ).first()
            
            if existing_user:
                logger.warning(f"Utilisateur déjà existant: {email}")
                return None
            
            new_user = User(
                email=email,
                username=username,
                password_hash=generate_password_hash(password)
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"✓ Utilisateur créé: {email}")
            
            return {
                'id': new_user.id,
                'email': new_user.email,
                'username': new_user.username
            }
            
        except Exception as e:
            logger.error(f"Erreur création utilisateur: {e}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authentifie un utilisateur
        
        Args:
            email: Email
            password: Mot de passe
        
        Returns:
            Token JWT + données utilisateur si succès, None sinon
        """
        try:
            from models import User
            from werkzeug.security import check_password_hash
            
            user = User.query.filter_by(email=email).first()
            
            if not user or not check_password_hash(user.password_hash, password):
                logger.warning(f"Authentification échouée pour: {email}")
                return None
            
            token = self.generate_jwt_token(user.id, user.email)
            
            return {
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username
                }
            }
            
        except Exception as e:
            logger.error(f"Erreur authentification: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du module d'authentification"""
        return {
            'enabled': self.enabled,
            'supabase_configured': self.supabase_url is not None,
            'jwt_enabled': True
        }


auth_service = AuthService()
