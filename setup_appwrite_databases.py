
#!/usr/bin/env python3
"""
Configuration Appwrite comme base de données de secours
Crée les databases et collections nécessaires
"""
import os
import sys

try:
    from appwrite.client import Client
    from appwrite.services.databases import Databases
    from appwrite.services.storage import Storage
    from appwrite.id import ID
except ImportError:
    print("❌ SDK Appwrite non installé. Installation...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "appwrite"])
    from appwrite.client import Client
    from appwrite.services.databases import Databases
    from appwrite.services.storage import Storage
    from appwrite.id import ID


def setup_appwrite():
    """Configure Appwrite pour être prêt comme backup"""
    
    print("\n" + "="*60)
    print("🟠 CONFIGURATION APPWRITE (BASE DE SECOURS)")
    print("="*60)
    
    endpoint = os.getenv('API_ENDPOINT_APPRWRITE')
    project_id = os.getenv('PROJET_ID_APPWRITE')
    api_key = os.getenv('API__KEY_APPWRITE')
    
    if not all([endpoint, project_id, api_key]):
        print("❌ Variables Appwrite manquantes!")
        print("Ajoutez dans Secrets:")
        print("  - API_ENDPOINT_APPRWRITE")
        print("  - PROJET_ID_APPWRITE")
        print("  - API__KEY_APPWRITE")
        return False
    
    try:
        # Initialiser client
        client = Client()
        client.set_endpoint(endpoint)
        client.set_project(project_id)
        client.set_key(api_key)
        
        databases = Databases(client)
        storage = Storage(client)
        
        # Créer la database principale
        database_id = 'profiles_db'
        
        try:
            db = databases.create(
                database_id=database_id,
                name='Profiles Database (Backup)'
            )
            print(f"✅ Database créée: {db['name']}")
        except Exception as e:
            if 'already exists' in str(e).lower():
                print(f"ℹ️  Database existe déjà")
            else:
                raise
        
        # Créer collections pour hommes et femmes
        for gender in ['men', 'women']:
            collection_id = f'profiles_{gender}'
            
            try:
                collection = databases.create_collection(
                    database_id=database_id,
                    collection_id=collection_id,
                    name=f'Profiles {gender.title()}'
                )
                print(f"✅ Collection créée: {collection['name']}")
                
                # Créer les attributs
                attributes = [
                    {'key': 'email', 'type': 'string', 'size': 255, 'required': True},
                    {'key': 'gender', 'type': 'string', 'size': 10, 'required': True},
                    {'key': 'first_name', 'type': 'string', 'size': 100, 'required': False},
                    {'key': 'last_name', 'type': 'string', 'size': 100, 'required': False},
                    {'key': 'birth_date', 'type': 'string', 'size': 10, 'required': False},
                    {'key': 'photo_ids', 'type': 'string', 'size': 1000, 'required': False, 'array': True},
                    {'key': 'professions', 'type': 'string', 'size': 5000, 'required': False},
                    {'key': 'professional_status', 'type': 'string', 'size': 5000, 'required': False},
                    {'key': 'interests', 'type': 'string', 'size': 5000, 'required': False},
                    {'key': 'favorite_books', 'type': 'string', 'size': 5000, 'required': False},
                    {'key': 'favorite_movies', 'type': 'string', 'size': 5000, 'required': False},
                    {'key': 'favorite_music', 'type': 'string', 'size': 5000, 'required': False},
                ]
                
                for attr in attributes:
                    try:
                        if attr.get('array'):
                            databases.create_string_attribute(
                                database_id=database_id,
                                collection_id=collection_id,
                                key=attr['key'],
                                size=attr['size'],
                                required=attr['required'],
                                array=True
                            )
                        else:
                            databases.create_string_attribute(
                                database_id=database_id,
                                collection_id=collection_id,
                                key=attr['key'],
                                size=attr['size'],
                                required=attr['required']
                            )
                        print(f"  ✓ Attribut: {attr['key']}")
                    except Exception as e:
                        if 'already exists' in str(e).lower():
                            print(f"  ℹ️  Attribut existe: {attr['key']}")
                        else:
                            print(f"  ⚠️  Erreur attribut {attr['key']}: {e}")
                
            except Exception as e:
                if 'already exists' in str(e).lower():
                    print(f"ℹ️  Collection existe déjà: {collection_id}")
                else:
                    raise
        
        # Créer buckets Storage
        for gender in ['men', 'women']:
            bucket_id = f'profiles-{gender}'
            
            try:
                bucket = storage.create_bucket(
                    bucket_id=bucket_id,
                    name=f'Profile Photos {gender.title()}',
                    permissions=[],
                    file_security=False,
                    enabled=True
                )
                print(f"✅ Bucket créé: {bucket['name']}")
            except Exception as e:
                if 'already exists' in str(e).lower():
                    print(f"ℹ️  Bucket existe déjà: {bucket_id}")
                else:
                    raise
        
        print("\n" + "="*60)
        print("✅ APPWRITE CONFIGURÉ COMME BASE DE SECOURS")
        print("="*60)
        print("En cas d'échec Supabase, Appwrite prendra automatiquement le relais")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration Appwrite: {e}")
        return False


if __name__ == '__main__':
    setup_appwrite()
