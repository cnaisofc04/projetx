"""
Service de collaboration
GitHub + GitLab + Trello
"""
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class CollaborationService:
    """
    Intégrations collaboration
    - GitHub: Repos, issues, PRs
    - GitLab: Projets, pipelines
    - Trello: Boards, cartes
    """
    
    def __init__(self):
        self.github_enabled = False
        self.gitlab_enabled = False
        self.trello_enabled = False
        self._initialize()
    
    def _initialize(self):
        """Initialise les services de collaboration"""
        from config.settings import Config
        keys = Config.get_api_keys()
        
        self.github_token = keys['github']['token']
        self.gitlab_token = keys['gitlab']['token']
        self.trello_key = keys['trello']['api_key']
        self.trello_token = keys['trello']['token']
        
        self.github_enabled = self.github_token is not None
        self.gitlab_enabled = self.gitlab_token is not None
        self.trello_enabled = self.trello_key is not None and self.trello_token is not None
        
        if self.github_enabled:
            logger.info("✓ GitHub activé")
        if self.gitlab_enabled:
            logger.info("✓ GitLab activé")
        if self.trello_enabled:
            logger.info("✓ Trello activé")
    
    def create_github_issue(self, repo: str, title: str, body: str) -> Optional[Dict]:
        """
        Crée une issue GitHub
        
        Args:
            repo: Nom du repo (format: owner/repo)
            title: Titre de l'issue
            body: Description
        
        Returns:
            Issue créée ou None
        """
        if not self.github_enabled:
            logger.error("GitHub non activé")
            return None
        
        try:
            from github import Github
            
            g = Github(self.github_token)
            repository = g.get_repo(repo)
            issue = repository.create_issue(title=title, body=body)
            
            logger.info(f"✓ GitHub issue créée: {issue.number}")
            
            return {
                'number': issue.number,
                'url': issue.html_url,
                'state': issue.state
            }
            
        except Exception as e:
            logger.error(f"Erreur création issue GitHub: {e}")
            return None
    
    def create_trello_card(self, list_id: str, name: str, desc: str = "") -> Optional[Dict]:
        """
        Crée une carte Trello
        
        Args:
            list_id: ID de la liste Trello
            name: Nom de la carte
            desc: Description
        
        Returns:
            Carte créée ou None
        """
        if not self.trello_enabled:
            logger.error("Trello non activé")
            return None
        
        try:
            import requests
            
            url = "https://api.trello.com/1/cards"
            params = {
                'key': self.trello_key,
                'token': self.trello_token,
                'idList': list_id,
                'name': name,
                'desc': desc
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            card = response.json()
            logger.info(f"✓ Carte Trello créée: {card['id']}")
            
            return {
                'id': card['id'],
                'url': card['url'],
                'name': card['name']
            }
            
        except Exception as e:
            logger.error(f"Erreur création carte Trello: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut des services de collaboration"""
        return {
            'github': {
                'enabled': self.github_enabled,
                'free_tier': 'Illimité pour repos publics'
            },
            'gitlab': {
                'enabled': self.gitlab_enabled,
                'free_tier': '400 CI minutes/mois'
            },
            'trello': {
                'enabled': self.trello_enabled,
                'free_tier': '10 boards illimités'
            }
        }


collaboration_service = CollaborationService()
