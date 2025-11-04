
"""
Routes pour la plateforme d'apprentissage API Academy
"""
from flask import Blueprint, render_template, jsonify, request
import logging
from typing import Dict, Any
from security.api_manager import api_key_manager

academy_bp = Blueprint('academy', __name__)
logger = logging.getLogger(__name__)

# Données des tutoriels pour chaque plateforme
PLATFORM_TUTORIALS = {
    'supabase': {
        'name': 'Supabase',
        'description': 'Backend complet avec PostgreSQL, Auth, Storage et Realtime',
        'icon': 'bi-database',
        'steps': [
            {
                'title': 'Installation et Configuration',
                'description': 'Installez le client Supabase et configurez votre projet',
                'code': '''from supabase import create_client, Client

url = "VOTRE_URL_SUPABASE"
key = "VOTRE_CLE_SUPABASE"
supabase: Client = create_client(url, key)

print("✅ Supabase connecté !")''',
                'try_it': True
            },
            {
                'title': 'Créer une table et insérer des données',
                'description': 'Utilisez la base de données PostgreSQL',
                'code': '''# Créer une table (via l'interface Supabase)
# Puis insérer des données

data = supabase.table('users').insert({
    'name': 'John Doe',
    'email': 'john@example.com'
}).execute()

print(f"Utilisateur créé : {data.data}")''',
                'try_it': True
            },
            {
                'title': 'Authentification utilisateur',
                'description': 'Gérez les inscriptions et connexions',
                'code': '''# Inscription
auth_response = supabase.auth.sign_up({
    'email': 'user@example.com',
    'password': 'password123'
})

# Connexion
session = supabase.auth.sign_in_with_password({
    'email': 'user@example.com',
    'password': 'password123'
})

print(f"Token : {session.session.access_token}")''',
                'try_it': False
            }
        ],
        'api_acquisition': [
            'Allez sur <a href="https://supabase.com" target="_blank">supabase.com</a>',
            'Créez un compte gratuit',
            'Créez un nouveau projet',
            'Dans Settings > API, copiez votre URL et clé anon/public',
            'Collez-les dans notre gestionnaire de secrets'
        ],
        'use_cases': ['SaaS', 'Applications mobiles', 'Dashboards temps réel']
    },
    'stripe': {
        'name': 'Stripe',
        'description': 'Plateforme de paiements en ligne complète',
        'icon': 'bi-credit-card',
        'steps': [
            {
                'title': 'Configuration Stripe',
                'description': 'Initialisez Stripe avec votre clé secrète',
                'code': '''import stripe

stripe.api_key = "VOTRE_CLE_SECRETE"

# Test de connexion
balance = stripe.Balance.retrieve()
print(f"Balance : {balance.available[0].amount / 100}€")''',
                'try_it': True
            },
            {
                'title': 'Créer un paiement',
                'description': 'Acceptez un paiement one-time',
                'code': '''# Créer un PaymentIntent
payment_intent = stripe.PaymentIntent.create(
    amount=2000,  # 20.00€ en centimes
    currency='eur',
    payment_method_types=['card']
)

# Client secret pour le frontend
client_secret = payment_intent.client_secret
print(f"Client secret : {client_secret}")''',
                'try_it': True
            },
            {
                'title': 'Créer un abonnement',
                'description': 'Gérez des paiements récurrents',
                'code': '''# Créer un client
customer = stripe.Customer.create(
    email='customer@example.com',
    name='John Doe'
)

# Créer un abonnement
subscription = stripe.Subscription.create(
    customer=customer.id,
    items=[{'price': 'price_xxxxx'}]  # ID de votre prix
)

print(f"Abonnement créé : {subscription.id}")''',
                'try_it': False
            }
        ],
        'api_acquisition': [
            'Créez un compte sur <a href="https://stripe.com" target="_blank">stripe.com</a>',
            'Activez votre compte (KYC)',
            'Allez dans Developers > API keys',
            'Copiez votre clé secrète (sk_test_... pour test)',
            'Stockez-la dans notre gestionnaire de secrets'
        ],
        'use_cases': ['E-commerce', 'SaaS', 'Marketplaces', 'Donations']
    },
    'openai': {
        'name': 'OpenAI',
        'description': 'API d\'Intelligence Artificielle (GPT-4, DALL-E, Whisper)',
        'icon': 'bi-cpu',
        'steps': [
            {
                'title': 'Configuration OpenAI',
                'description': 'Initialisez le client OpenAI',
                'code': '''from openai import OpenAI

client = OpenAI(api_key="VOTRE_CLE_API")

# Test
models = client.models.list()
print(f"✅ {len(models.data)} modèles disponibles")''',
                'try_it': True
            },
            {
                'title': 'Chat avec GPT-4',
                'description': 'Créez un chatbot intelligent',
                'code': '''response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Tu es un assistant utile."},
        {"role": "user", "content": "Explique-moi Python en 3 phrases"}
    ]
)

print(response.choices[0].message.content)''',
                'try_it': True
            },
            {
                'title': 'Générer des images',
                'description': 'Utilisez DALL-E pour créer des images',
                'code': '''image = client.images.generate(
    prompt="Un chat qui code en Python",
    n=1,
    size="1024x1024"
)

print(f"Image URL : {image.data[0].url}")''',
                'try_it': False
            }
        ],
        'api_acquisition': [
            'Créez un compte sur <a href="https://platform.openai.com" target="_blank">platform.openai.com</a>',
            'Ajoutez un moyen de paiement (payant après 5$)',
            'Allez dans API keys',
            'Créez une nouvelle clé secrète',
            'Copiez-la et stockez-la en sécurité'
        ],
        'use_cases': ['Chatbots', 'Génération de contenu', 'Assistants virtuels', 'Analyse de documents']
    },
    'github': {
        'name': 'GitHub',
        'description': 'Gestion de code, CI/CD, et collaboration',
        'icon': 'bi-github',
        'steps': [
            {
                'title': 'Authentification GitHub',
                'description': 'Connectez-vous à l\'API GitHub',
                'code': '''from github import Github

g = Github("VOTRE_TOKEN")

# Récupérer votre profil
user = g.get_user()
print(f"Bonjour {user.name} !")
print(f"Repos publics : {user.public_repos}")''',
                'try_it': True
            },
            {
                'title': 'Lister vos repositories',
                'description': 'Accédez à vos projets',
                'code': '''for repo in g.get_user().get_repos():
    print(f"📦 {repo.name} - ⭐ {repo.stargazers_count} stars")''',
                'try_it': True
            },
            {
                'title': 'Créer une issue',
                'description': 'Automatisez la gestion de bugs',
                'code': '''repo = g.get_repo("username/repo")

issue = repo.create_issue(
    title="Bug trouvé",
    body="Description du bug...",
    labels=["bug"]
)

print(f"Issue créée : {issue.html_url}")''',
                'try_it': False
            }
        ],
        'api_acquisition': [
            'Connectez-vous à <a href="https://github.com" target="_blank">github.com</a>',
            'Allez dans Settings > Developer settings > Personal access tokens',
            'Générez un nouveau token (classic)',
            'Sélectionnez les scopes (repo, user, etc.)',
            'Copiez le token et sauvegardez-le'
        ],
        'use_cases': ['Automatisation DevOps', 'CI/CD', 'Gestion de projets', 'Backup automatique']
    }
    # ... Ajoutez les 20 autres plateformes
}

@academy_bp.route('/')
def home():
    """Page d'accueil de l'academy"""
    return render_template('academy_home.html')

@academy_bp.route('/learn/<platform_id>')
def learn_platform(platform_id: str):
    """Page de tutoriel pour une plateforme"""
    if platform_id not in PLATFORM_TUTORIALS:
        return "Plateforme non trouvée", 404
    
    platform_data = PLATFORM_TUTORIALS[platform_id]
    
    return render_template(
        'learn_platform.html',
        platform_id=platform_id,
        platform_name=platform_data['name'],
        platform_description=platform_data['description'],
        platform_data=platform_data
    )

@academy_bp.route('/api/test-platform', methods=['POST'])
def test_platform():
    """Test une connexion à une plateforme"""
    data = request.json
    platform = data.get('platform')
    api_key = data.get('api_key')
    
    # Tests de validation
    if platform == 'stripe':
        try:
            import stripe
            stripe.api_key = api_key
            balance = stripe.Balance.retrieve()
            return jsonify({
                'success': True,
                'message': f'Balance : {balance.available[0].amount / 100}€'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    elif platform == 'openai':
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            models = client.models.list()
            return jsonify({
                'success': True,
                'message': f'{len(models.data)} modèles disponibles'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    # ... Ajoutez d'autres plateformes
    
    return jsonify({'success': False, 'error': 'Plateforme non supportée'})

@academy_bp.route('/secrets-manager')
def secrets_manager():
    """Interface de gestion des secrets"""
    return render_template('secrets_manager.html')

@academy_bp.route('/api/secrets', methods=['GET'])
def get_secrets():
    """Récupère tous les secrets (masqués)"""
    all_secrets = api_key_manager.get_all_platforms_status()
    
    # Format pour l'interface
    secrets_by_platform = {}
    for platform_id, status in all_secrets.items():
        if status['available_keys']:
            secrets_by_platform[platform_id] = {
                key: '***' for key in status['available_keys']
            }
    
    return jsonify({'secrets': secrets_by_platform})
