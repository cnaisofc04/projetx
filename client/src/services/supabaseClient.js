import { createClient } from '@supabase/supabase-js';

// ============================================
// CONFIGURATION DOUBLE INSTANCE SUPABASE
// ============================================

// Variables pour Supabase HOMMES
const supabaseManUrl = import.meta.env.VITE_SUPABASE_MAN_URL;
const supabaseManAnonKey = import.meta.env.VITE_SUPABASE_MAN_ANON_KEY;

// Variables pour Supabase FEMMES  
const supabaseWomanUrl = import.meta.env.VITE_SUPABASE_WOMAN_URL;
const supabaseWomanAnonKey = import.meta.env.VITE_SUPABASE_WOMAN_ANON_KEY;

console.log('🔧 Supabase MAN URL:', supabaseManUrl);
console.log('🔧 Supabase MAN Key présente:', supabaseManAnonKey ? '✅ Oui' : '❌ Non');
console.log('🔧 Supabase WOMAN URL:', supabaseWomanUrl);
console.log('🔧 Supabase WOMAN Key présente:', supabaseWomanAnonKey ? '✅ Oui' : '❌ Non');

// Validation des variables d'environnement
if (!supabaseManUrl || !supabaseManAnonKey || !supabaseWomanUrl || !supabaseWomanAnonKey) {
  console.error('❌ ERREUR: Variables Supabase manquantes dans client/.env');
  console.error('Ajoutez VITE_SUPABASE_MAN_URL, VITE_SUPABASE_MAN_ANON_KEY');
  console.error('et VITE_SUPABASE_WOMAN_URL, VITE_SUPABASE_WOMAN_ANON_KEY');
}

// Créer les clients Supabase (hommes et femmes)
export const supabaseMan = createClient(supabaseManUrl, supabaseManAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  }
});

export const supabaseWoman = createClient(supabaseWomanUrl, supabaseWomanAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  }
});

// Fonction pour obtenir le bon client selon le genre
const getSupabaseClient = (gender) => {
  return gender === 'man' ? supabaseMan : supabaseWoman;
};

// ============================================
// FONCTION: Sauvegarder le profil complet
// ============================================
export const saveProfile = async (email, profileData) => {
  try {
    console.log('📤 Tentative de sauvegarde profil pour:', email);
    console.log('📦 Données:', profileData);

    const gender = profileData.gender;
    const supabase = getSupabaseClient(gender);
    const bucketName = gender === 'man' ? 'avatars-men' : 'avatars-women';

    // 1. Upload des photos si présentes
    let photoUrls = [];
    if (profileData.photos && profileData.photos.length > 0) {
      console.log(`📸 Upload de ${profileData.photos.length} photos vers ${bucketName}`);

      for (let i = 0; i < profileData.photos.length; i++) {
        const photo = profileData.photos[i];

        // Convertir base64 en blob
        const base64Data = photo.split(',')[1];
        const byteCharacters = atob(base64Data);
        const byteNumbers = new Array(byteCharacters.length);
        for (let j = 0; j < byteCharacters.length; j++) {
          byteNumbers[j] = byteCharacters.charCodeAt(j);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'image/jpeg' });

        // Upload vers Storage
        const fileName = `${email}/photo_${i}.jpg`;
        const { data: uploadData, error: uploadError } = await supabase.storage
          .from(bucketName)
          .upload(fileName, blob, {
            cacheControl: '3600',
            upsert: true
          });

        if (uploadError) {
          console.error('❌ Erreur upload photo:', uploadError);
          throw uploadError;
        }

        // Récupérer l'URL publique
        const { data: urlData } = supabase.storage
          .from(bucketName)
          .getPublicUrl(fileName);

        photoUrls.push(urlData.publicUrl);
        console.log(`✅ Photo ${i + 1} uploadée:`, urlData.publicUrl);
      }
    }

    // 2. Insérer le profil dans la table
    const profileToSave = {
      email: email,
      gender: gender,
      first_name: profileData.firstName,
      last_name: profileData.lastName,
      birth_date: profileData.birthDate,
      photos: photoUrls,
      professions: profileData.professions || [],
      interests: profileData.interests || [],
      favorite_books: profileData.favoriteBooks || [],
      favorite_movies: profileData.favoriteMovies || [],
      favorite_music: profileData.favoriteMusic || []
    };

    console.log('💾 Sauvegarde profil:', profileToSave);

    const { data, error } = await supabase
      .from('profiles')
      .insert([profileToSave])
      .select();

    if (error) {
      console.error('❌ Erreur Supabase:', error);
      throw new Error(`Erreur base de données: ${error.message}`);
    }

    console.log('✅ Profil sauvegardé avec succès:', data);
    return { success: true, data: data[0] };

  } catch (error) {
    console.error('❌ Erreur sauvegarde profil:', error);
    throw {
      message: error.message || 'Erreur inconnue',
      details: error.details || 'Vérifiez que la table "profiles" existe dans Supabase'
    };
  }
};

// Export par défaut (pour compatibilité)
export const supabase = supabaseMan;

// ============================================
// FONCTION: Récupérer un profil
// ============================================
export const getProfile = async (userId) => {
  try {
    // Le client Supabase à utiliser dépend du genre, mais pour une récupération simple,
    // nous devons potentiellement interroger les deux bases ou avoir une logique plus complexe ici.
    // Pour l'instant, utilisons manSupabase comme défaut, mais cela devra être affiné.
    const { data, error } = await supabaseMan
      .from('profiles')
      .select('*')
      .eq('user_id', userId)
      .single();

    if (error && error.code !== 'PGRST116') { // PGRST116 = not found
      throw error;
    }

    return { data, error: null };
  } catch (error) {
    console.error('❌ Erreur récupération profil:', error);
    return { data: null, error };
  }
};

// ============================================
// FONCTION: Upload photo
// ============================================
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

// ============================================
// FONCTION: Test de connexion
// ============================================
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