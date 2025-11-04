import os
from typing import Dict, Any


class Config:
    """Configuration centralisée pour toute l'application"""
    
    SECRET_KEY = os.environ.get("SESSION_SECRET")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DEBUG = os.environ.get("FLASK_ENV") == "development"
    TESTING = False
    
    @staticmethod
    def get_api_keys() -> Dict[str, Any]:
        """Retourne toutes les clés API disponibles de manière sécurisée"""
        return {
            'openai': {
                'primary': os.environ.get("OPEN_AI_API_KEY"),
                'test_node': os.environ.get("Try_out_Your_new_API_key_NODE"),
                'test_python': os.environ.get("Try_out_your_new_API_key_Python"),
                'manus': os.environ.get("MANUS_API_KEY"),
            },
            'stripe': {
                'public': os.environ.get("STRIPE_API_KEY_PUBLIC"),
                'secret': os.environ.get("STRIPE_API_KEY_SECRET"),
            },
            'supabase': {
                'url': os.environ.get("URL_SUPABASE_AUTOQG"),
                'anon_public': os.environ.get("SUPABASE_ANON_PUBLIC"),
                'api_key': os.environ.get("SUPABASE_AUTOQG_API_KEY"),
                'role_secret': os.environ.get("SUPABASE_ROLE_SECRET"),
                'secret': os.environ.get("api_key_secret_supabase"),
            },
            'redis': {
                'url': os.environ.get("REDIS_URL_us_east_1"),
                'api_key': os.environ.get("REDIS_API_KEY"),
                'cache_id': os.environ.get("REDIS_CACHE_ID"),
                'cli': os.environ.get("REDIS_CLI"),
                'service_name': os.environ.get("REDIS_SERVICE_NAME"),
                'account_key': os.environ.get("REDIS_API_account_key"),
                'generated_key': os.environ.get("REDIS_API_KEY_GENERATED_LangCache"),
            },
            'github': {
                'token': os.environ.get("GITHUB_TOKEN_API"),
            },
            'gitlab': {
                'token': os.environ.get("TOKEN_API_GITLAB"),
            },
            'trello': {
                'api_key': os.environ.get("TRELLO_API_KEY"),
                'token': os.environ.get("TRELLO_TOKEN"),
            },
            'resend': {
                'api_key': os.environ.get("RESEND_API_KEY"),
            },
            'appwrite': {
                'endpoint': os.environ.get("API_ENDPOINT_APPRWRITE"),
                'project_id': os.environ.get("PROJET_ID_APPWRITE"),
            },
            'amplitude': {
                'api_key': os.environ.get("AMPLITUDE_API_KEY"),
                'server_url': os.environ.get("AMPLITUDE_Standard_Server_url"),
                'eu_url': os.environ.get("AMPLITUDE_EU_Residency_Server_URL"),
            },
            'logrocket': {
                'app_id': os.environ.get("LOG_ROCKET_App_ID"),
                'api_key': os.environ.get("LOG_ROCKET_API_KEY"),
                'project_name': os.environ.get("LOG_ROCKET_Project_Name"),
            },
            'agora': {
                'app_id': os.environ.get("AGORA_APP_ID"),
                'primary_cert': os.environ.get("AGORA_Primary_Certificate"),
                'secondary_cert': os.environ.get("AGORA_Secondary_Certificate"),
            },
            'mapbox': {
                'access_token': os.environ.get("MAPBOX_ACCESS_TOKEN"),
            },
            'airtable': {
                'api_key': os.environ.get("AIRTABLE_API_KEY"),
            },
            'posthog': {
                'api_key': os.environ.get("POSTHOG_API_KEY"),
            },
            'expo': {
                'api_key': os.environ.get("EXPO_API_KEY"),
            },
            'pipedream': {
                'workspace_id': os.environ.get("PIPEDREAM_Workspace_ID"),
                'client_id': os.environ.get("PIPEDREAM_API_KEY_Client_ID"),
                'client_secret': os.environ.get("PIPEDREAM_API_KEY_Client_Secret"),
            },
            'flowith': {
                'api_key': os.environ.get("FLOWITH_API_KEY"),
            },
            'gabriel': {
                'api_key_1': os.environ.get("GABRIEL_API_KEY_1"),
            },
        }


class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
