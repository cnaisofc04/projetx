# 🚀 RAPPORT TEST NOUVELLES API
**Date**: 2025-10-27 16:22:49  
**Tests**: 14  
**Réussis**: 10 (71.4%)  
**Échecs**: 1

---

## 📋 RÉSUMÉ PAR API

### ⚠️ Amplitude (1/2)

✅ **Configuration Clé**: SUCCESS
   - Clé API présente

⚠️ **Envoi Event**: WARNING
   - Status 400

### ✅ GitHub (1/1)

✅ **Quick Check**: SUCCESS
   - User: cnaisofc04

### ✅ GitLab (1/1)

✅ **Quick Check**: SUCCESS
   - Auth OK

### ⚠️ LogRocket (1/2)

✅ **Configuration Clé**: SUCCESS
   - Clé API présente (frontend JS requis)

⚠️ **API REST**: WARNING
   - Status 403 (vérifier clé)

### ⚠️ OpenAI (2/3)

✅ **Initialisation Client**: SUCCESS
   - Client créé

✅ **Liste Modèles**: SUCCESS
   - Modèles: gpt-3.5-turbo, gpt-5-search-api-2025-10-14, gpt-audio-mini-2025-10-06

❌ **Chat Completion**: ERROR
   - ❌ `Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}`

### ❌ Redis (0/1)

⚠️ **Configuration URL**: WARNING
   - REDIS_URL non configurée

### ✅ Resend (1/1)

✅ **Quick Check**: SUCCESS
   - API OK

### ✅ Stripe (1/1)

✅ **Quick Check**: SUCCESS
   - Account: acct_1SM7zi2LOg5Xc155

### ✅ Supabase (1/1)

✅ **Quick Check**: SUCCESS
   - Client créé

### ✅ Trello (1/1)

✅ **Quick Check**: SUCCESS
   - User: cnaisofc02


---

## 📊 STATISTIQUES GLOBALES

- **Total tests**: 14
- **Succès**: 10 (71.4%)
- **Échecs**: 1
- **Warnings**: 3

🟡 **BON** - La plupart des API fonctionnent

---

*Rapport généré automatiquement*
