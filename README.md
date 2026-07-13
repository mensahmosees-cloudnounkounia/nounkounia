# Nounkoun — IA agricole du Bénin

## Structure

```
app.py                  ← webhook Flask/Twilio (point d'entrée WhatsApp)
requirements.txt
nounkoun/
  __init__.py            ← expose repondre() ET traiter_message()
  data.py                 ← TOUTES les connaissances (cultures, sols, techniques,
                             intrants, glossaire paysan, calendrier lunaire,
                             signes visuels pour le diagnostic)
  matcher.py              ← reconnaît QUELLE culture est citée dans le message
  intents.py              ← reconnaît QUOI l'utilisateur demande (prix / calendrier
                             / recette / problème / info générale)
  responder.py            ← assemble la réponse finale (repondre()) — comportement V1-V5
  communes.py             ← table GPS statique des communes du Bénin
  db.py                   ← persistance SQLite (paysans, alertes)
  location.py             ← enregistrement GPS + recherche de paysans proches
  diagnostic.py           ← diagnostic par DESCRIPTION texte (pas de vraie vision)
  community.py            ← prépare les alertes à envoyer aux paysans voisins
  dispatcher.py           ← V6 : route GPS / photo / diagnostic / communauté /
                             sinon retombe sur responder.repondre()
```

`app.py` utilise `traiter_message()` (V6, avec GPS/communauté) qui retombe sur
`repondre()` (V1-V5) dès qu'aucune fonctionnalité V6 n'est concernée. Les deux
restent exposées et indépendantes de Flask/Twilio.

## Nouveautés V6 — ce qui a été corrigé par rapport à votre code collé

1. **`USERS_DB = {}` en mémoire → SQLite (`db.py`)**. Un dict Python ne
   survit pas à un redémarrage, et n'est pas partagé entre plusieurs
   workers Flask en production. Un fichier `nounkoun.db` réglé une fois
   pour toutes.
2. **Géocodage Nominatim en direct → table statique (`communes.py`)**.
   Nominatim limite à 1 requête/seconde et n'est pas fiable dans un
   webhook qui doit répondre vite. La liste des communes du Bénin ne
   change pas : autant la figer.
3. **"IA Vision" avec un faux `% de confiance` → `diagnostic.py` honnête**.
   L'ancien code prétendait analyser la photo alors qu'il ne lisait que le
   texte tapé par l'utilisateur, et affichait un pourcentage
   (`score * 30`) qui n'a aucune valeur statistique réelle. Renommé en
   "diagnostic par description", sans faux pourcentage — pour ne pas
   qu'un paysan traite sa parcelle sur la foi d'un chiffre inventé.
4. **Bug d'extraction de commune** : l'ancien code faisait
   `message.replace("a", "")` sur toute la chaîne, ce qui mangeait aussi
   les "a" internes ("à Allada" devenait "à llada"). Corrigé pour ne
   retirer que la préposition en tête de phrase.
5. **Séparation décision/envoi pour les alertes** : `community.py` décide
   QUI prévenir et QUOI dire, `app.py` (qui a les identifiants Twilio) fait
   l'envoi réel. Ça permet de tester la logique sans dépendre de Twilio.

## Sur le smart contract Solidity et le dashboard V8

Je ne les ai pas intégrés à ce stade — voir mon message dans la conversation
pour le détail, en résumé :
- Le contrat NFT suppose un wallet crypto/gas pour chaque paysan, ce qui ne
  colle pas à un usage 100% WhatsApp/SMS.
- Le dashboard référence des variables (`USERS_DB_V8`, `DICO_TUBERCULES_V8`)
  qui n'existent dans aucun fichier fourni — il plante à l'import.
- Les deux ne sont connectés à rien du backend actuel.

Recommandation d'ordre réaliste : stabiliser V6 (GPS + communauté +
diagnostic) en usage réel avec quelques dizaines de paysans, AVANT
d'ajouter dashboard/blockchain/drone — ce sont des projets indépendants,
pas des incréments naturels du chatbot.

## Ce qui a été corrigé par rapport à vos versions v1-v4

1. **5 copies identiques de v4** collées dans le message → gardé une seule
   version, fusionnée avec les infos uniques de v1/v2/v3 (coton, riz, sorgho,
   mil, sols, agroécologie... qui n'existaient que dans les versions
   antérieures et avaient disparu en v4).
2. **Faux positifs de matching** : `"mais" in message` matchait aussi
   "fran**çais**" ou "j**amais**". `matcher.py` matche maintenant sur des
   mots entiers.
3. **Accents/caractères Fon (ɔ, ɛ, é...)** : un paysan qui tape sans accent
   sur son téléphone ("mais" au lieu de "maïs", "te" au lieu de "tè") ne
   matchait plus rien. `normaliser()` gère ça des deux côtés.
4. **Toutes les données dans une seule fonction géante** avec des blocs
   `if/elif` empilés → séparé en 4 responsabilités claires (données /
   reconnaissance culture / reconnaissance intention / réponse), donc chaque
   ajout futur touche un seul fichier.
5. **Liste de cultures "je connais..." codée en dur** dans le message
   d'erreur → générée dynamiquement depuis `data.py`, jamais désynchronisée.

## Feuille de route v5 → v8

- **v5 — Couverture** : ajouter les cultures maraîchères (tomate, piment,
  gombo, légumes-feuilles) et l'arachide/niébé/soja, qui manquent encore.
  Il suffit d'ajouter une entrée dans `CULTURES` (`data.py`) ; rien d'autre
  à toucher.
- **v6 — Robustesse du matching** : remplacer le matching exact par une
  distance de Levenshtein tolérante (ex: bibliothèque `rapidfuzz`) pour
  absorber les fautes de frappe (`"mannioc"`, `"cotton"`).
- **v7 — Mémoire de conversation** : garder le dernier `culture_id` par
  numéro de téléphone (Redis ou simple dict avec expiration) pour que
  `"et le prix ?"` après `"mon manioc est malade"` fonctionne sans redire
  "manioc".
- **v8 — Contenu enrichi** : passer les `solutions_naturelles` et
  `problemes` en liens vers photos (WhatsApp Media) et audio en langues
  locales (accessibilité pour les paysans non-lettrés), et brancher un
  vrai modèle de langage en secours quand `trouver_culture()` ne matche
  rien, plutôt que le message d'erreur statique.

## Lancer en local

```bash
pip install -r requirements.txt
python app.py
```
