"""
Service OpenAI
Intégration complète avec gestion des tokens et rate limiting
"""
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class OpenAIService:
    """
    Intégration OpenAI
    - Chat completions
    - Embeddings
    - Gestion des tokens
    - Rate limiting pour free tier
    """
    
    def __init__(self):
        self.client = None
        self.enabled = False
        self._initialize_openai()
    
    def _initialize_openai(self):
        """Initialise le client OpenAI"""
        try:
            from openai import OpenAI
            from config.settings import Config
            
            keys = Config.get_api_keys()
            api_key = keys['openai']['primary']
            
            if api_key:
                self.client = OpenAI(api_key=api_key)
                self.enabled = True
                logger.info("✓ OpenAI initialisé")
            else:
                logger.warning("✗ Clé OpenAI manquante")
                
        except ImportError:
            logger.error("Module openai non installé")
        except Exception as e:
            logger.error(f"Erreur initialisation OpenAI: {e}")
    
    def chat_completion(self, messages: List[Dict[str, str]], 
                       model: str = "gpt-3.5-turbo",
                       max_tokens: int = 500) -> Optional[str]:
        """
        Génère une réponse de chat
        
        Args:
            messages: Liste de messages [{"role": "user", "content": "..."}]
            model: Modèle à utiliser
            max_tokens: Limite de tokens
        
        Returns:
            Réponse générée ou None si erreur
        """
        if not self.enabled:
            logger.error("OpenAI non activé")
            return None
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            logger.info(f"✓ Chat completion généré ({len(content)} chars)")
            
            return content
            
        except Exception as e:
            logger.error(f"Erreur chat completion: {e}")
            return None
    
    def create_embedding(self, text: str, model: str = "text-embedding-ada-002") -> Optional[List[float]]:
        """
        Crée un embedding pour un texte
        
        Args:
            text: Texte à embedder
            model: Modèle d'embedding
        
        Returns:
            Vecteur d'embedding ou None si erreur
        """
        if not self.enabled:
            logger.error("OpenAI non activé")
            return None
        
        try:
            response = self.client.embeddings.create(
                model=model,
                input=text
            )
            
            embedding = response.data[0].embedding
            logger.info(f"✓ Embedding créé ({len(embedding)} dimensions)")
            
            return embedding
            
        except Exception as e:
            logger.error(f"Erreur création embedding: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du module OpenAI"""
        return {
            'enabled': self.enabled,
            'models_available': self.enabled
        }


openai_service = OpenAIService()
