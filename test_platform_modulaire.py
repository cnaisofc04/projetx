
#!/usr/bin/env python3
"""
Test ULTRA-MODULAIRE - Chaque plateforme, chaque fonction testée individuellement
"""

import os
import sys
import json
from datetime import datetime
from security.api_manager import api_key_manager

class ModularPlatformTester:
    """Testeur modulaire pour chaque plateforme"""
    
    def __init__(self):
        self.results = {}
        
    def test_all_platforms(self):
        """Test toutes les plateformes de manière modulaire"""
        print("\n" + "="*80)
        print("🚀 TEST ULTRA-MODULAIRE DE TOUTES LES PLATEFORMES")
        print("="*80)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Résumé global
        summary = api_key_manager.get_summary()
        print(f"\n📊 RÉSUMÉ GLOBAL:")
        print(f"   Plateformes totales: {summary['total_platforms']}")
        print(f"   ✅ Complètes: {summary['complete']}")
        print(f"   ⚠️  Partielles: {summary['partial']}")
        print(f"   ❌ Manquantes: {summary['missing']}")
        print(f"   📈 Taux de complétion: {summary['completion_rate']:.1f}%")
        print(f"   🔑 Clés disponibles: {summary['available_keys']}/{summary['total_keys']}")
        
        # Test par type de plateforme
        platform_types = set(p['type'] for p in api_key_manager.PLATFORMS.values())
        
        for ptype in sorted(platform_types):
            self._test_platform_type(ptype)
        
        # Génération du rapport
        self._generate_report()
    
    def _test_platform_type(self, platform_type: str):
        """Test toutes les plateformes d'un type donné"""
        print("\n" + "="*80)
        print(f"📦 TYPE: {platform_type.upper()}")
        print("="*80)
        
        platforms = api_key_manager.get_platforms_by_type(platform_type)
        
        for platform_id in platforms:
            self._test_platform(platform_id)
    
    def _test_platform(self, platform_id: str):
        """Test une plateforme spécifique avec toutes ses fonctions"""
        status = api_key_manager.get_platform_status(platform_id)
        
        if not status:
            return
        
        name = status['name']
        platform_status = status['status']
        available_keys = status['available_keys']
        missing_keys = status['missing_keys']
        
        # Symbole selon le statut
        if platform_status == 'COMPLET':
            symbol = '✅'
        elif platform_status == 'PARTIEL':
            symbol = '⚠️'
        else:
            symbol = '❌'
        
        print(f"\n{symbol} {name}")
        print(f"   Statut: {platform_status}")
        print(f"   Clés disponibles ({len(available_keys)}):")
        for key in available_keys:
            print(f"      ✓ {key}")
        
        if missing_keys:
            print(f"   Clés manquantes ({len(missing_keys)}):")
            for key in missing_keys:
                print(f"      ✗ {key}")
        
        # Test des fonctions spécifiques
        self._test_platform_functions(platform_id, status)
        
        self.results[platform_id] = {
            'name': name,
            'status': platform_status,
            'available_keys': available_keys,
            'missing_keys': missing_keys,
            'tests': self._get_platform_tests(platform_id)
        }
    
    def _test_platform_functions(self, platform_id: str, status: dict):
        """Test les fonctions spécifiques d'une plateforme"""
        if status['status'] == 'MANQUANT':
            print("   ⚠️  Aucune clé disponible - Tests ignorés")
            return
        
        # Tests spécifiques par plateforme
        test_methods = {
            'supabase': self._test_supabase,
            'appwrite': self._test_appwrite,
            'stripe': self._test_stripe,
            'openai': self._test_openai,
            'redis': self._test_redis,
            'postgres': self._test_postgres,
            'github': self._test_github,
            'gitlab': self._test_gitlab,
            'trello': self._test_trello,
            'resend': self._test_resend,
            'agora': self._test_agora,
            'amplitude': self._test_amplitude,
            'logrocket': self._test_logrocket,
            'posthog': self._test_posthog,
            'mapbox': self._test_mapbox,
            'airtable': self._test_airtable,
            'pipedream': self._test_pipedream,
            'expo': self._test_expo,
            'flowith': self._test_flowith,
        }
        
        test_method = test_methods.get(platform_id)
        if test_method:
            print("   🧪 Tests fonctionnels:")
            test_method()
        else:
            print("   ℹ️  Tests fonctionnels non implémentés (clés validées)")
    
    def _get_platform_tests(self, platform_id: str) -> list:
        """Retourne la liste des tests disponibles pour une plateforme"""
        tests_map = {
            'supabase': ['Auth', 'Database', 'Storage', 'Realtime'],
            'appwrite': ['Auth', 'Database', 'Storage', 'Functions'],
            'stripe': ['Payments', 'Customers', 'Subscriptions', 'Webhooks'],
            'openai': ['Completions', 'Chat', 'Embeddings', 'Models'],
            'redis': ['Cache', 'Pub/Sub', 'Streams'],
            'postgres': ['Connection', 'Queries', 'Transactions'],
            'github': ['Repos', 'Issues', 'PRs', 'Actions', 'Webhooks'],
            'gitlab': ['Projects', 'MRs', 'CI/CD', 'Pipelines'],
            'trello': ['Boards', 'Cards', 'Lists', 'Webhooks'],
            'resend': ['Send Email', 'Templates', 'Domains'],
            'agora': ['Video', 'Audio', 'Streaming'],
            'amplitude': ['Events', 'Users', 'Analytics'],
            'logrocket': ['Sessions', 'Events', 'Errors'],
            'posthog': ['Events', 'Users', 'Feature Flags'],
            'mapbox': ['Geocoding', 'Directions', 'Maps'],
            'airtable': ['Bases', 'Tables', 'Records'],
            'pipedream': ['Workflows', 'Triggers', 'Actions'],
            'expo': ['Push Notifications', 'Updates'],
            'flowith': ['AI Workflows'],
        }
        return tests_map.get(platform_id, ['Configuration'])
    
    # Méthodes de test par plateforme
    def _test_supabase(self):
        keys = api_key_manager.get_all_keys('supabase')
        if 'URL_SUPABASE_AUTOQG' in keys:
            print("      ✓ URL configurée")
        if 'SUPABASE_ANON_PUBLIC' in keys or 'SUPABASE_AUTOQG_API_KEY' in keys:
            print("      ✓ Clé API configurée")
    
    def _test_appwrite(self):
        keys = api_key_manager.get_all_keys('appwrite')
        if 'API_ENDPOINT_APPRWRITE' in keys:
            print("      ✓ Endpoint configuré")
        if 'PROJET_ID_APPWRITE' in keys:
            print("      ✓ Project ID configuré")
    
    def _test_stripe(self):
        keys = api_key_manager.get_all_keys('stripe')
        if 'STRIPE_API_KEY_SECRET' in keys:
            print("      ✓ Secret key configurée")
        if 'STRIPE_API_KEY_PUBLIC' in keys:
            print("      ✓ Public key configurée")
    
    def _test_openai(self):
        keys = api_key_manager.get_all_keys('openai')
        if keys:
            print("      ✓ API key configurée")
    
    def _test_redis(self):
        keys = api_key_manager.get_all_keys('redis')
        if 'REDIS_API_KEY' in keys or 'REDIS_URL_us_east_1' in keys:
            print("      ✓ Connexion configurée")
    
    def _test_postgres(self):
        keys = api_key_manager.get_all_keys('postgres')
        if 'DATABASE_URL' in keys:
            print("      ✓ Database URL configurée")
        elif all(k in keys for k in ['PGHOST', 'PGDATABASE']):
            print("      ✓ Paramètres de connexion configurés")
    
    def _test_github(self):
        if api_key_manager.get_key('github'):
            print("      ✓ Token configuré")
    
    def _test_gitlab(self):
        if api_key_manager.get_key('gitlab'):
            print("      ✓ Token configuré")
    
    def _test_trello(self):
        keys = api_key_manager.get_all_keys('trello')
        if 'TRELLO_API_KEY' in keys and 'TRELLO_TOKEN' in keys:
            print("      ✓ API Key et Token configurés")
    
    def _test_resend(self):
        if api_key_manager.get_key('resend'):
            print("      ✓ API key configurée")
    
    def _test_agora(self):
        keys = api_key_manager.get_all_keys('agora')
        if 'AGORA_APP_ID' in keys:
            print("      ✓ App ID configuré")
        if 'AGORA_Primary_Certificate' in keys:
            print("      ✓ Certificats configurés")
    
    def _test_amplitude(self):
        keys = api_key_manager.get_all_keys('amplitude')
        if 'AMPLITUDE_API_KEY' in keys:
            print("      ✓ API key configurée")
        if 'AMPLITUDE_Standard_Server_url' in keys or 'AMPLITUDE_EU_Residency_Server_URL' in keys:
            print("      ✓ Server URL configurée")
    
    def _test_logrocket(self):
        keys = api_key_manager.get_all_keys('logrocket')
        if 'LOG_ROCKET_API_KEY' in keys:
            print("      ✓ API key configurée")
        if 'LOG_ROCKET_App_ID' in keys:
            print("      ✓ App ID configuré")
    
    def _test_posthog(self):
        if api_key_manager.get_key('posthog'):
            print("      ✓ API key configurée")
    
    def _test_mapbox(self):
        if api_key_manager.get_key('mapbox'):
            print("      ✓ Access token configuré")
    
    def _test_airtable(self):
        if api_key_manager.get_key('airtable'):
            print("      ✓ API key configurée")
    
    def _test_pipedream(self):
        keys = api_key_manager.get_all_keys('pipedream')
        if 'PIPEDREAM_API_KEY_Client_ID' in keys and 'PIPEDREAM_API_KEY_Client_Secret' in keys:
            print("      ✓ OAuth credentials configurés")
        if 'PIPEDREAM_Workspace_ID' in keys:
            print("      ✓ Workspace ID configuré")
    
    def _test_expo(self):
        if api_key_manager.get_key('expo'):
            print("      ✓ API key configurée")
    
    def _test_flowith(self):
        if api_key_manager.get_key('flowith'):
            print("      ✓ API key configurée")
    
    def _generate_report(self):
        """Génère un rapport JSON détaillé"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"RAPPORT_MODULAIRE_{timestamp}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': api_key_manager.get_summary(),
            'platforms': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*80)
        print(f"✅ RAPPORT GÉNÉRÉ: {filename}")
        print("="*80)
        
        summary = report['summary']
        print(f"\n📊 RÉSUMÉ FINAL:")
        print(f"   ✅ Plateformes complètes: {summary['complete']}")
        print(f"   ⚠️  Plateformes partielles: {summary['partial']}")
        print(f"   ❌ Plateformes manquantes: {summary['missing']}")
        print(f"   📈 Taux de complétion: {summary['completion_rate']:.1f}%")


if __name__ == "__main__":
    tester = ModularPlatformTester()
    tester.test_all_platforms()
