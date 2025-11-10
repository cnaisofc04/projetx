
"""
Gestionnaire de base de données avec fallback automatique
Supabase (prioritaire) → Appwrite (backup)
"""
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Gestionnaire unifié avec fallback automatique:
    1. Tente Supabase d'abord
    2. Si échec, bascule vers Appwrite
    """
    
    def __init__(self):
        self.primary_db = "supabase"  # Base de données principale
        self.fallback_db = "appwrite"  # Base de données de secours
        self.current_db = None
        
        # Clients initialisés
        self.supabase_men = None
        self.supabase_women = None
        self.appwrite_client = None
        
        self._initialize_databases()
    
    def _initialize_databases(self):
        """Initialise toutes les connexions disponibles"""
        
        # === SUPABASE ===
        try:
            from supabase import create_client
            
            # Hommes
            man_url = os.getenv('profil_man_supabase_URL')
            man_key = os.getenv('profil_man_supabase_API_service_role_secret')
            
            if man_url and man_key:
                self.supabase_men = create_client(man_url, man_key)
                logger.info("✅ Supabase HOMMES initialisé")
            
            # Femmes
            woman_url = os.getenv('profil_woman_supabase_URL')
            woman_key = os.getenv('profil_woman_supabase_API_service_role_secret')
            
            if woman_url and woman_key:
                self.supabase_women = create_client(woman_url, woman_key)
                logger.info("✅ Supabase FEMMES initialisé")
                
        except Exception as e:
            logger.warning(f"⚠️ Supabase non disponible: {e}")
        
        # === APPWRITE ===
        try:
            from appwrite.client import Client
            from appwrite.services.databases import Databases
            from appwrite.services.storage import Storage
            
            endpoint = os.getenv('API_ENDPOINT_APPRWRITE')
            project_id = os.getenv('PROJET_ID_APPWRITE')
            api_key = os.getenv('API__KEY_APPWRITE')
            
            if endpoint and project_id and api_key:
                client = Client()
                client.set_endpoint(endpoint)
                client.set_project(project_id)
                client.set_key(api_key)
                
                self.appwrite_client = {
                    'client': client,
                    'databases': Databases(client),
                    'storage': Storage(client)
                }
                logger.info("✅ Appwrite initialisé (backup)")
            
        except Exception as e:
            logger.warning(f"⚠️ Appwrite non disponible: {e}")
    
    def _get_supabase_client(self, gender: str):
        """Récupère le client Supabase selon le genre"""
        if gender.lower() == 'woman':
            return self.supabase_women
        return self.supabase_men
    
    def create_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée un profil avec fallback automatique
        1. Essaie Supabase
        2. Si échec, utilise Appwrite
        """
        gender = profile_data.get('gender', 'man').lower()
        
        # === TENTATIVE SUPABASE ===
        supabase_client = self._get_supabase_client(gender)
        
        if supabase_client:
            try:
                logger.info(f"🔵 Tentative Supabase ({gender})...")
                
                # Séparer les photos
                photos = profile_data.pop('photos', [])
                photo_urls = []
                
                # Upload photos vers Supabase Storage
                bucket = 'avatars-men' if gender == 'man' else 'avatars-women'
                
                for i, photo_base64 in enumerate(photos):
                    if photo_base64.startswith('data:image'):
                        import base64
                        header, encoded = photo_base64.split(',', 1)
                        file_data = base64.b64decode(encoded)
                        
                        file_path = f"{profile_data['email']}/photo_{i}.png"
                        
                        supabase_client.storage.from_(bucket).upload(
                            file_path, file_data,
                            {'content-type': 'image/png', 'upsert': 'true'}
                        )
                        
                        url = supabase_client.storage.from_(bucket).get_public_url(file_path)
                        photo_urls.append(url)
                
                profile_data['photos'] = photo_urls
                
                # Insérer le profil
                result = supabase_client.table('profiles').insert(profile_data).execute()
                
                self.current_db = "supabase"
                logger.info(f"✅ Profil créé sur Supabase ({gender})")
                
                return {
                    'success': True,
                    'database': 'supabase',
                    'data': result.data
                }
                
            except Exception as e:
                logger.warning(f"⚠️ Supabase échoué: {e}")
                logger.info("🔄 Basculement vers Appwrite...")
        
        # === FALLBACK APPWRITE ===
        if self.appwrite_client:
            try:
                logger.info(f"🟠 Utilisation Appwrite (backup)...")
                
                databases = self.appwrite_client['databases']
                storage = self.appwrite_client['storage']
                
                # Upload photos vers Appwrite Storage
                photos = profile_data.pop('photos', [])
                photo_ids = []
                
                bucket_id = 'profiles-men' if gender == 'man' else 'profiles-women'
                
                for i, photo_base64 in enumerate(photos):
                    if photo_base64.startswith('data:image'):
                        import base64
                        from appwrite.input_file import InputFile
                        
                        header, encoded = photo_base64.split(',', 1)
                        file_data = base64.b64decode(encoded)
                        
                        # Créer un fichier temporaire
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                            tmp.write(file_data)
                            tmp_path = tmp.name
                        
                        # Upload
                        file_id = f"{profile_data['email']}_photo_{i}"
                        file_result = storage.create_file(
                            bucket_id=bucket_id,
                            file_id=file_id,
                            file=InputFile.from_path(tmp_path)
                        )
                        
                        photo_ids.append(file_result['$id'])
                        
                        # Nettoyer
                        import os as os_module
                        os_module.unlink(tmp_path)
                
                profile_data['photo_ids'] = photo_ids
                
                # Convertir les tableaux en JSON pour Appwrite
                for key in ['professions', 'professional_status', 'interests', 
                           'favorite_books', 'favorite_movies', 'favorite_music']:
                    if key in profile_data and isinstance(profile_data[key], list):
                        import json
                        profile_data[key] = json.dumps(profile_data[key])
                
                # Insérer dans Appwrite Database
                database_id = os.getenv('APPWRITE_DATABASE_ID', 'profiles_db')
                collection_id = 'profiles_men' if gender == 'man' else 'profiles_women'
                
                from appwrite.id import ID
                result = databases.create_document(
                    database_id=database_id,
                    collection_id=collection_id,
                    document_id=ID.unique(),
                    data=profile_data
                )
                
                self.current_db = "appwrite"
                logger.info(f"✅ Profil créé sur Appwrite (backup) ({gender})")
                
                return {
                    'success': True,
                    'database': 'appwrite',
                    'data': result
                }
                
            except Exception as e:
                logger.error(f"❌ Appwrite aussi échoué: {e}")
                raise Exception(f"Aucune base de données disponible. Supabase et Appwrite ont échoué.")
        
        raise Exception("Aucune base de données configurée")
    
    def get_profile(self, email: str, gender: str) -> Optional[Dict[str, Any]]:
        """Récupère un profil avec fallback"""
        
        # Essayer Supabase d'abord
        supabase_client = self._get_supabase_client(gender)
        
        if supabase_client:
            try:
                result = supabase_client.table('profiles').select('*').eq('email', email).execute()
                if result.data:
                    self.current_db = "supabase"
                    return result.data[0]
            except Exception as e:
                logger.warning(f"Supabase échec: {e}")
        
        # Fallback Appwrite
        if self.appwrite_client:
            try:
                from appwrite.query import Query
                
                databases = self.appwrite_client['databases']
                database_id = os.getenv('APPWRITE_DATABASE_ID', 'profiles_db')
                collection_id = 'profiles_men' if gender == 'man' else 'profiles_women'
                
                result = databases.list_documents(
                    database_id=database_id,
                    collection_id=collection_id,
                    queries=[Query.equal('email', email)]
                )
                
                if result['documents']:
                    self.current_db = "appwrite"
                    return result['documents'][0]
                    
            except Exception as e:
                logger.error(f"Appwrite échec: {e}")
        
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """Statut des bases de données"""
        return {
            'supabase': {
                'men': self.supabase_men is not None,
                'women': self.supabase_women is not None
            },
            'appwrite': self.appwrite_client is not None,
            'current_active': self.current_db
        }


# Instance globale
db_manager = DatabaseManager()
