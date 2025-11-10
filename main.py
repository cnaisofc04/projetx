from app import app
import logging

logging.basicConfig(level=logging.DEBUG)

@app.route('/api/save-profile', methods=['POST'])
def save_profile():
    """Endpoint pour sauvegarder le profil utilisateur"""
    try:
        from supabase import create_client
        import os
        
        # Récupérer les données
        data = request.get_json()
        
        # Initialiser Supabase
        supabase = create_client(
            os.getenv('URL_SUPABASE_AUTOQG'),
            os.getenv('api_key_secret_supabase')  # Utiliser la clé secrète côté serveur
        )
        
        # Séparer les photos des autres données
        photos = data.pop('photos', [])
        
        # D'abord, uploader les photos vers Supabase Storage
        photo_urls = []
        for i, photo_base64 in enumerate(photos):
            if photo_base64.startswith('data:image'):
                # Extraire le type et les données
                import base64
                header, encoded = photo_base64.split(',', 1)
                file_data = base64.b64decode(encoded)
                
                # Upload vers Storage
                file_path = f"{data['email']}/photo_{i}.png"
                supabase.storage.from_('avatars').upload(
                    file_path,
                    file_data,
                    {'content-type': 'image/png'}
                )
                
                # Récupérer l'URL publique
                url = supabase.storage.from_('avatars').get_public_url(file_path)
                photo_urls.append(url)
        
        # Remplacer les photos base64 par les URLs
        data['photos'] = photo_urls
        
        # Insérer le profil
        result = supabase.table('profiles').insert(data).execute()
        
        return jsonify({
            'success': True,
            'data': result.data
        })
        
    except Exception as e:
        print(f'❌ Erreur sauvegarde: {str(e)}')
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
