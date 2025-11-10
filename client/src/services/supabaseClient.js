/**
 * Service de sauvegarde des profils
 * Utilise l'API Flask backend avec fallback automatique Supabase → Appwrite
 */

const API_BASE_URL = window.location.origin;

export const supabase = {
  /**
   * Sauvegarde un profil via l'API Flask
   * Le backend gère automatiquement le fallback Supabase → Appwrite
   */
  async saveProfile(profileData) {
    console.log('📤 Sauvegarde profil via API Flask:', profileData.email);

    try {
      const response = await fetch(`${API_BASE_URL}/api/save-profile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData)
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Erreur de sauvegarde');
      }

      const result = await response.json();
      console.log('✅ Profil sauvegardé:', result.database);

      return result;
    } catch (error) {
      console.error('❌ Erreur sauvegarde:', error);
      throw error;
    }
  },

  /**
   * Récupère un profil
   */
  async getProfile(email, gender) {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/get-profile?email=${encodeURIComponent(email)}&gender=${gender}`
      );

      if (!response.ok) {
        throw new Error('Profil non trouvé');
      }

      return await response.json();
    } catch (error) {
      console.error('❌ Erreur récupération profil:', error);
      throw error;
    }
  }
};

// Export par défaut (pour compatibilité)
// This export is removed as the new supabase object is intended to replace the previous one entirely.
// export const supabase = supabaseMan;

// ============================================
// FONCTION: Sauvegarder le profil complet
// ============================================
// This function is now replaced by the saveProfile method within the new supabase object.
// export const saveProfile = async (email, profileData) => { ... };

// ============================================
// FONCTION: Récupérer un profil
// ============================================
// This function is now replaced by the getProfile method within the new supabase object.
// export const getProfile = async (userId) => { ... };

// ============================================
// FONCTION: Upload photo
// ============================================
// The uploadPhoto function is not directly replaced by the new supabase object.
// If photo uploads are still needed directly, a new implementation using the Flask API would be required.
// For now, we'll comment it out as the primary focus was on profile saving/retrieval via Flask.
/*
export const uploadPhoto = async (file, userId) => {
  // Cette fonction doit aussi être mise à jour pour utiliser le bon bucket basé sur le genre de l'utilisateur.
  // Pour l'instant, elle utilise un bucket générique 'photos' qui pourrait ne plus exister.
  // Il faudrait passer le genre de l'utilisateur pour déterminer le bon bucket.
  try {
    const fileExt = file.name.split('.').pop();
    const fileName = `${userId}/${Date.now()}.${fileExt}`;

    console.log('📤 Upload photo:', fileName);

    // Upload vers Supabase Storage
    const { data: uploadData, error: uploadError } = await supabaseMan.storage // Utilisation de supabaseMan par défaut
      .from('photos') // Ce bucket pourrait devoir être renommé ou géré différemment
      .upload(fileName, file, {
        cacheControl: '3600',
        upsert: false
      });

    if (uploadError) {
      console.error('❌ Erreur upload:', uploadError);
      throw uploadError;
    }

    // Obtenir l'URL publique
    const { data: { publicUrl } } = supabaseMan.storage // Utilisation de supabaseMan par défaut
      .from('photos') // Ce bucket pourrait devoir être renommé ou géré différemment
      .getPublicUrl(fileName);

    console.log('✅ Photo uploadée:', publicUrl);

    return {
      data: {
        path: fileName,
        url: publicUrl
      },
      error: null
    };

  } catch (error) {
    console.error('❌ Erreur upload photo:', error);
    return {
      data: null,
      error: {
        message: error.message,
        details: 'Vérifiez que le bucket "photos" existe dans Supabase Storage'
      }
    };
  }
};
*/

// ============================================
// FONCTION: Test de connexion
// ============================================
// This function is also not directly replaced. If a connection test is needed,
// it should now target the Flask API.
/*
export const testConnection = async () => {
  try {
    // Test de connexion avec le client par défaut (supabaseMan)
    const { data, error } = await supabaseMan
      .from('profiles')
      .select('count')
      .limit(1);

    if (error) {
      console.error('❌ Connexion Supabase échouée:', error);
      return false;
    }

    console.log('✅ Connexion Supabase OK');
    return true;
  } catch (error) {
    console.error('❌ Erreur test connexion:', error);
    return false;
  }
};
*/