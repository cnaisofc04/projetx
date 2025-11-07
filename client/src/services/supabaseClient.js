
import { createClient } from '@supabase/supabase-js'

// Configuration Supabase depuis les variables d'environnement
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://votre-projet.supabase.co'
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'votre-cle-publique'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Service de stockage photos
export const uploadPhoto = async (file, userId) => {
  const fileExt = file.name.split('.').pop()
  const fileName = `${userId}/${Date.now()}.${fileExt}`
  
  const { data, error } = await supabase.storage
    .from('profile-photos')
    .upload(fileName, file)
  
  if (error) throw error
  
  // Récupérer l'URL publique
  const { data: { publicUrl } } = supabase.storage
    .from('profile-photos')
    .getPublicUrl(fileName)
  
  return publicUrl
}

// Service de sauvegarde profil
export const saveProfile = async (userId, profileData) => {
  const { data, error } = await supabase
    .from('profiles')
    .upsert({
      id: userId,
      ...profileData,
      updated_at: new Date().toISOString()
    })
  
  if (error) throw error
  return data
}

// Service de récupération profil
export const getProfile = async (userId) => {
  const { data, error } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', userId)
    .single()
  
  if (error) throw error
  return data
}
