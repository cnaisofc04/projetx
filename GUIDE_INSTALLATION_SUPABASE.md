
# 🚀 GUIDE D'INSTALLATION SUPABASE

## Étape 1 : Créer un compte Supabase

1. Allez sur **https://supabase.com**
2. Cliquez sur **"Start your project"**
3. Connectez-vous avec GitHub ou email

## Étape 2 : Créer un nouveau projet

1. Cliquez sur **"New Project"**
2. Choisissez un nom (ex: `dating-app`)
3. Créez un mot de passe de base de données (NOTEZ-LE!)
4. Sélectionnez la région la plus proche
5. Cliquez sur **"Create new project"**
6. ⏳ Attendez 2-3 minutes que le projet se crée

## Étape 3 : Récupérer les clés API

1. Dans le menu gauche, cliquez sur **⚙️ Settings**
2. Cliquez sur **API**
3. Vous verrez :
   - **Project URL** (ex: `https://abcdefgh.supabase.co`)
   - **anon/public key** (une très longue chaîne)

4. Copiez ces 2 valeurs dans `client/.env` :

```env
VITE_SUPABASE_URL=https://votreprojet.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Étape 4 : Créer la base de données

1. Dans le menu gauche, cliquez sur **🗄️ SQL Editor**
2. Cliquez sur **"New Query"**
3. Ouvrez le fichier `supabase_schema.sql` dans ce projet
4. Copiez TOUT le contenu
5. Collez-le dans l'éditeur SQL
6. Cliquez sur **"Run"** (ou Ctrl+Enter)
7. ✅ Vous devriez voir "Success. No rows returned"

## Étape 5 : Vérifier la table

1. Dans le menu gauche, cliquez sur **📊 Table Editor**
2. Vous devriez voir la table **`profiles`**
3. Cliquez dessus pour voir les colonnes

## Étape 6 : Configurer le Storage

1. Dans le menu gauche, cliquez sur **🗂️ Storage**
2. Vérifiez que le bucket **`photos`** existe
3. Si non, le schéma SQL l'a créé automatiquement

## Étape 7 : Tester la connexion

1. Dans Replit, exécutez :
```bash
cd client && npm run dev
```

2. Ouvrez la console du navigateur (F12)
3. Vous devriez voir : **"✅ Connexion Supabase OK"**

## ❌ Problèmes courants

### Erreur: "relation profiles does not exist"
➡️ **Solution:** Vous n'avez pas exécuté `supabase_schema.sql`

### Erreur: "Invalid API key"
➡️ **Solution:** Vérifiez que vous avez bien copié la clé **anon/public** (pas la clé service!)

### Erreur: "bucket photos does not exist"
➡️ **Solution:** Réexécutez la partie Storage du fichier SQL

## ✅ Tout fonctionne !

Vous êtes prêt ! L'application peut maintenant :
- ✅ Sauvegarder les profils
- ✅ Uploader des photos
- ✅ Récupérer les données
