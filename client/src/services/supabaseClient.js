
import { createClient } from '@supabase/supabase-js';

// 🔹 CONFIGURATION DYNAMIQUE: Hommes OU Femmes selon le contexte utilisateur
// Par défaut, utiliser la base HOMMES (sera changé dynamiquement après login)
const supabaseUrl = import.meta.env.VITE_SUPABASE_MAN_URL || import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_MAN_ANON_KEY || import.meta.env.VITE_SUPABASE_ANON_KEY;

console.log('🔧 Supabase URL:', supabaseUrl);
console.log('🔧 Supabase Key présente:', supabaseAnonKey ? '✅ Oui' : '❌ Non');
console.log('🔧 Mode:', 'Profils (Hommes/Femmes séparés)');

// Validation des variables d'environnement
if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ ERREUR: Variables Supabase manquantes dans .env');
  console.error('Ajoutez VITE_SUPABASE_URL et VITE_SUPABASE_ANON_KEY');
}

if (supabaseUrl?.includes('votre-projet') || supabaseAnonKey?.includes('votre_cle')) {
  console.error('❌ ERREUR: Remplacez les valeurs par défaut dans client/.env');
  console.error('Allez sur https://supabase.com/dashboard > Settings > API');
}

// Créer le client Supabase
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  }
});

// ============================================
// FONCTION: Sauvegarder le profil complet
// ============================================
export const saveProfile = async (userId, profileData) => {
  try {
    console.log('📤 Tentative de sauvegarde profil pour:', userId);
    console.log('📦 Données:', profileData);

    // Préparer les données
    const dataToSave = {
      user_id: userId,
      email: profileData.email || userId,
      first_name: profileData.firstName,
      last_name: profileData.lastName,
      birth_date: profileData.birthDate,
      gender: profileData.gender,
      eye_color: profileData.eyeColor,
      hair_color: profileData.hairColor,
      religion: profileData.religion,
      beard_preference: profileData.beardPreference,
      relationship_type: profileData.relationshipType,
      sexual_orientation: profileData.sexualOrientation,
      photos: profileData.photos || [],
      professions: profileData.professions || [],
      professional_status: profileData.professionalStatus || [],
      interests: profileData.interests || [],
      favorite_books: profileData.favoriteBooks || [],
      favorite_movies: profileData.favoriteMovies || [],
      favorite_music: profileData.favoriteMusic || [],
      psychology_questions: profileData.psychologyQuestions || {},
      detailed_preferences: profileData.detailedPreferences || {},
      privacy_zone: profileData.privacyZone || {},
      updated_at: new Date().toISOString()
    };

    // Utiliser upsert pour insert OU update
    const { data, error } = await supabase
      .from('profiles')
      .upsert(dataToSave, {
        onConflict: 'user_id'
      })
      .select();

    if (error) {
      console.error('❌ Erreur Supabase:', error);
      throw new Error(`Erreur base de données: ${error.message}`);
    }

    console.log('✅ Profil sauvegardé avec succès:', data);
    return { data, error: null };

  } catch (error) {
    console.error('❌ Erreur sauvegarde profil:', error);
    return { 
      data: null, 
      error: {
        message: error.message,
        details: 'Vérifiez que la table "profiles" existe dans Supabase'
      }
    };
  }
};

// ============================================
// FONCTION: Récupérer un profil
// ============================================
export const getProfile = async (userId) => {
  try {
    const { data, error } = await supabase
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
  try {
    const fileExt = file.name.split('.').pop();
    const fileName = `${userId}/${Date.now()}.${fileExt}`;

    console.log('📤 Upload photo:', fileName);

    // Upload vers Supabase Storage
    const { data: uploadData, error: uploadError } = await supabase.storage
      .from('photos')
      .upload(fileName, file, {
        cacheControl: '3600',
        upsert: false
      });

    if (uploadError) {
      console.error('❌ Erreur upload:', uploadError);
      throw uploadError;
    }

    // Obtenir l'URL publique
    const { data: { publicUrl } } = supabase.storage
      .from('photos')
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
    const { data, error } = await supabase
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
