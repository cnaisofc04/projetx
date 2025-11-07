import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

// Créer le vrai client Supabase
export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Fonction pour sauvegarder le profil complet
export const saveProfile = async (userId, profileData) => {
  try {
    // Sauvegarder dans la table profiles
    const { data, error } = await supabase
      .from('profiles')
      .upsert({
        user_id: userId,
        ...profileData,
        updated_at: new Date().toISOString()
      })
      .select();

    if (error) throw error;

    console.log('✅ Profil sauvegardé avec succès:', data);
    return { data, error: null };
  } catch (error) {
    console.error('❌ Erreur sauvegarde profil:', error);
    return { data: null, error };
  }
};

// Fonction pour récupérer un profil
export const getProfile = async (userId) => {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .select('*')
      .eq('user_id', userId)
      .single();

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error('❌ Erreur récupération profil:', error);
    return { data: null, error };
  }
};

// Fonction pour uploader une photo
export const uploadPhoto = async (file, userId) => {
  try {
    const fileExt = file.name.split('.').pop();
    const fileName = `${userId}/${Date.now()}.${fileExt}`;

    const { data, error } = await supabase.storage
      .from('photos')
      .upload(fileName, file);

    if (error) throw error;

    const { data: { publicUrl } } = supabase.storage
      .from('photos')
      .getPublicUrl(fileName);

    return { data: { path: fileName, url: publicUrl }, error: null };
  } catch (error) {
    console.error('❌ Erreur upload photo:', error);
    return { data: null, error };
  }
};