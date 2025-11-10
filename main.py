from app import app
import logging

logging.basicConfig(level=logging.DEBUG)

@app.route('/api/save-profile', methods=['POST'])
def save_profile():
    """
    Endpoint pour sauvegarder le profil utilisateur
    ✅ AVEC FALLBACK AUTOMATIQUE Supabase → Appwrite
    """
    try:
        from modules.database.database_manager import db_manager
        
        # Récupérer les données
        data = request.get_json()
        
        # Créer le profil avec fallback automatique
        result = db_manager.create_profile(data)
        
        return jsonify(result)
        
    except Exception as e:
        print(f'❌ Erreur sauvegarde: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Échec de sauvegarde sur toutes les bases de données'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
