"""
Dashboard centralisé pour monitorer tous les modules
"""
from flask import Blueprint, render_template, jsonify
from datetime import datetime
from typing import Dict, Any
import logging

dashboard_bp = Blueprint('dashboard', __name__)
logger = logging.getLogger(__name__)


@dashboard_bp.route('/')
def index():
    """Page d'accueil avec dashboard des modules"""
    return render_template('dashboard.html')


@dashboard_bp.route('/api/status')
def api_status():
    """API retournant le statut de tous les modules"""
    try:
        from modules.auth.auth_service import auth_service
        from modules.payments.stripe_service import stripe_service
        from modules.cache.redis_service import redis_service
        from modules.ai.openai_service import openai_service
        from modules.analytics.analytics_service import analytics_service
        from modules.communication.communication_service import communication_service
        from modules.collaboration.collaboration_service import collaboration_service
        from modules.geolocation.mapbox_service import mapbox_service
        from modules.services.additional_services import additional_services
        from security.api_manager import api_key_manager

        status = {
            'timestamp': datetime.now().isoformat(),
            'modules': {
                'auth': auth_service.get_status(),
                'payments': stripe_service.get_status(),
                'cache': redis_service.get_status(),
                'ai': openai_service.get_status(),
                'analytics': analytics_service.get_status(),
                'communication': communication_service.get_status(),
                'collaboration': collaboration_service.get_status(),
                'geolocation': mapbox_service.get_status(),
                'additional_services': additional_services.get_status(),
            },
            'security': {
                'api_keys_status': api_key_manager.get_all_platforms_status()
            }
        }

        return jsonify(status)

    except Exception as e:
        logger.error(f"Erreur récupération statut: {e}")
        return jsonify({'error': str(e)}), 500