
# 🔴 COMMENT OBTENIR LES URLS REDIS CORRECTES

## ⚠️ IMPORTANT : L'API Account Key N'EST PAS une URL de connexion !

Vous avez actuellement dans vos secrets :
- `REDIS_API_account_key` = `A36a06esoxxeeSqxmb4enxBsUw5xNHxexzbxv24Nzqxxmt` ✅

Mais ce n'est **PAS** l'URL de connexion pour Redis !

---

## 📍 COMMENT TROUVER LES VRAIES URLs

### ÉTAPE 1 : Aller dans votre console Redis Cloud

1. Connectez-vous à https://app.redislabsredis://default:LDR68KZDSO3H7kdvLUQ71Zh2Tvln0UHG@redis-13195.c339.eu-west-3-1.ec2.redns.redis-cloud.com:13195redis://default:LDR68KZDSO3H7kdvLUQ71Zh2Tvln0UHG@redis-13195.c339.eu-west-3-1.ec2.redns.redis-cloud.com:13195redis://default:LDR68KZDSO3H7kdvLUQ71Zh2Tvln0UHG@redis-13195.c339.eu-west-3-1.ec2.redns.redis-cloud.com:13195redis://default:LDR68KZDSO3H7kdvLUQ71Zh2Tvln0UHG@redis-13195.c339.eu-west-3-1.ec2.redns.redis-cloud.com:13195.com/
2. Dans le menu latéral, cliquez sur **"Databases"**
3. Vous devriez voir une liste de vos bases de données Redis

### ÉTAPE 2 : Pour CHAQUE région (us-east-1, us-west-2, etc.)

1. Cliquez sur la base de données correspondante
2. Cherchez la section **"Connect"** ou **"Configuration"**
3. Vous devriez voir une **"Connection String"** ou **"Endpoint"**

### ÉTAPE 3 : Copier l'URL au bon format

L'URL doit ressembler à :

```
redis://default:VotreMOTdePASSE@redis-12345.c123.us-east-1-2.ec2.cloud.redislabs.com:12345
```

OU

```
rediss://default:VotreMOTdePASSE@redis-12345.c123.us-east-1-2.ec2.cloud.redislabs.com:12345
```

---

## 📋 SECRETS À REMPLIR DANS REPLIT

Une fois que vous avez récupéré les URLs depuis Redis Cloud Console :

### Pour REDIS_API_KEY
```
REDIS_API_KEY = redis://default:VotreMOTdePASSE@redis-xxxxx.c123.us-east-1-2.ec2.cloud.redislabs.com:12345
```

### Pour REDIS_URL_us_east_1
```
REDIS_URL_us_east_1 = redis://default:VotreMOTdePASSE@redis-xxxxx.c123.us-east-1-2.ec2.cloud.redislabs.com:12345
```

### Pour REDIS_URL_us_west_2
```
REDIS_URL_us_west_2 = redis://default:VotreMOTdePASSE@redis-xxxxx.c123.us-west-2-1.ec2.cloud.redislabs.com:12345
```

### Pour REDIS_URL_ap_south_1
```
REDIS_URL_ap_south_1 = redis://default:VotreMOTdePASSE@redis-xxxxx.c123.ap-south-1.ec2.cloud.redislabs.com:12345
```

### Pour REDIS_URL_us_east_4
```
REDIS_URL_us_east_4 = redis://default:VotreMOTdePASSE@redis-xxxxx.c123.us-east4.gcp.cloud.redislabs.com:12345
```

---

## 🎯 SI VOUS N'AVEZ QU'UNE SEULE BASE REDIS

Si vous n'avez créé qu'**une seule** base de données Redis, vous pouvez :

1. Utiliser la **MÊME URL** pour tous les secrets `REDIS_URL_*`
2. Ou supprimer les secrets régionaux inutiles

---

## 🔍 ALTERNATIVE : Chercher dans les détails de la base

Dans Redis Cloud Console :

1. Cliquez sur votre base de données
2. Cherchez l'onglet **"Configuration"** ou **"Connect"**
3. Vous devriez voir :
   - **Public endpoint** (l'URL complète)
   - **Password** (si vous l'avez sauvegardé)
   - **Port**

4. Construisez l'URL comme ceci :
   ```
   redis://default:VOTRE_PASSWORD@PUBLIC_ENDPOINT:PORT
   ```

---

## ⚠️ SI VOUS NE TROUVEZ PAS LE MOT DE PASSE

Si vous ne trouvez plus le mot de passe Redis :

1. Dans Redis Cloud Console → Votre base de données
2. Cherchez l'option **"Reset password"**
3. Générez un nouveau mot de passe
4. **COPIEZ-LE IMMÉDIATEMENT** (vous ne pourrez plus le revoir !)
5. Mettez à jour l'URL avec le nouveau mot de passe

---

## ✅ VÉRIFICATION FINALE

Une fois que vous avez mis à jour les secrets, lancez ce test :

```bash
python guide_recuperation_secrets.py
```

Vous devriez voir :
- ✅ REDIS_API_KEY - Format redis:// détecté
- ✅ REDIS_URL_us_east_1 - Connexion réussie
- etc.
