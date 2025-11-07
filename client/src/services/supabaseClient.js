import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

let supabase = null;

if (supabaseUrl && supabaseAnonKey && supabaseUrl !== 'your_supabase_url' && supabaseAnonKey !== 'your_anon_key') {
  try {
    supabase = createClient(supabaseUrl, supabaseAnonKey);
    console.log('✅ Supabase initialisé');
  } catch (error) {
    console.warn('❌ Erreur initialisation Supabase:', error.message);
  }
} else {
  console.warn('⚠️ Supabase non configuré - Mode local activé');
}

export { supabase };

// Service de stockage photos
export const uploadPhoto = async (file, userId) => {
  if (!supabase) {
    console.error("Supabase n'est pas initialisé. Impossible d'uploader la photo.");
    return null;
  }
  const fileExt = file.name.split('.').pop();
  const fileName = `${userId}/${Date.now()}.${fileExt}`;

  const { data, error } = await supabase.storage
    .from('profile-photos')
    .upload(fileName, file);

  if (error) {
    console.error("Erreur Supabase lors de l'upload de la photo:", error.message);
    throw error;
  }

  // Récupérer l'URL publique
  const { data: { publicUrl } } = supabase.storage
    .from('profile-photos')
    .getPublicUrl(fileName);

  return publicUrl;
}

// Service de sauvegarde profil
export const saveProfile = async (userId, profileData) => {
  if (!supabase) {
    console.error("Supabase n'est pas initialisé. Impossible de sauvegarder le profil.");
    return null;
  }
  const { data, error } = await supabase
    .from('profiles')
    .upsert({
      id: userId,
      ...profileData,
      updated_at: new Date().toISOString()
    });

  if (error) {
    console.error("Erreur Supabase lors de la sauvegarde du profil:", error.message);
    throw error;
  }
  return data;
}

// Service de récupération profil
export const getProfile = async (userId) => {
  if (!supabase) {
    console.error("Supabase n'est pas initialisé. Impossible de récupérer le profil.");
    return null;
  }
  const { data, error } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', userId)
    .single();

  if (error) {
    console.error("Erreur Supabase lors de la récupération du profil:", error.message);
    throw error;
  }
  return data;
}