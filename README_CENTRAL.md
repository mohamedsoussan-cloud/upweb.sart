# The Printing Yassine — passage en client-serveur

## Ce qui a changé
- Les comptes sont enregistrés dans `users` avec un hash Werkzeug (aucun mot de passe en clair).
- Connexion par e-mail, session Flask et route `POST /logout`.
- Les routes de gestion et les API sont protégées par une session.
- Le stockage métier `app_storage` utilise SQLAlchemy et la variable `DATABASE_URL` : PostgreSQL recommandé pour l'hébergement central.
- `desktop.py` est maintenant un client Windows : il ouvre l'URL HTTPS du serveur central. Il ne démarre plus une base locale.
- `create_user.py` permet à l'administrateur de créer des comptes supplémentaires.

## Étape 1 — créer une base PostgreSQL
Créez une base PostgreSQL chez votre hébergeur (par exemple Render PostgreSQL, Supabase ou un VPS). Copiez l'URL de connexion privée fournie par le prestataire. Ne publiez jamais cette URL.

## Étape 2 — déployer le serveur
1. Déposez les fichiers source sur un dépôt Git privé ou sur votre serveur.
2. Configurez la commande de démarrage `gunicorn app:app` (le `Procfile` la fournit).
3. Définissez les variables d'environnement dans le tableau de bord de l'hébergeur :
   - `DATABASE_URL` : URL PostgreSQL
   - `SECRET_KEY` : chaîne aléatoire longue et secrète
   - `ADMIN_EMAIL` : e-mail du premier administrateur
   - `ADMIN_PASSWORD` : mot de passe initial d'au moins 12 caractères
   - `COOKIE_SECURE=true` lorsque le site est servi en HTTPS
4. Déployez. Au démarrage, les tables `users`, `app_storage` et `app_meta` sont créées automatiquement. Le premier compte admin est créé si son e-mail n'existe pas encore.
5. Ouvrez `https://votre-serveur/api/health`. Le résultat attendu est `{"ok":true,"database":"postgresql"}`.
6. Connectez-vous à `https://votre-serveur/login`.

**Important :** ne mettez pas `.env`, `DATABASE_URL`, les mots de passe ou les secrets dans Git. Utilisez les variables secrètes du fournisseur. Pour Supabase, utilisez une URL PostgreSQL compatible avec psycopg et la configuration réseau recommandée par Supabase.

## Étape 3 — transférer les données de l'ancien PC
La base SQLite locale n'est pas transférée automatiquement. Fermez l'ancienne application, faites une copie de sauvegarde de :
`%LOCALAPPDATA%\The Printing Yassine\printing_yassine_data.db`

Sur un environnement Python configuré avec la `DATABASE_URL` de production, exécutez une seule fois :
```powershell
python migrate_local_data.py "C:\chemin\vers\printing_yassine_data.db"
```
Contrôlez les quantités, opérations et historique sur le serveur avant de distribuer le client. Gardez la sauvegarde jusqu'à validation complète.

## Étape 4 — créer les autres utilisateurs
Sur un terminal connecté à la même base centrale et avec `DATABASE_URL` définie :
```powershell
python create_user.py
```
Choisissez `user` pour un utilisateur normal ou `admin` pour un administrateur. Les comptes ne sont pas créés depuis l'écran de connexion.

## Étape 5 — configurer et compiler l'application Windows
1. Ouvrez `server_url.json.example`, remplacez l'URL par votre adresse HTTPS, puis enregistrez le fichier sous `server_url.json`.
2. Lancez `build_exe.bat` sur un PC Windows avec Python installé.
3. Distribuez **tout** le dossier `dist\The Printing Yassine\` (pas uniquement le `.exe`). Il contient `server_url.json`.
4. Chaque PC utilise le même serveur et donc la même base de données. Une connexion Internet est nécessaire.

Pour changer le serveur après compilation, modifiez `server_url.json` à côté du `.exe`.

## Limite importante — synchronisation simultanée
L'interface d'origine stocke les données dans le navigateur (`localStorage`) puis envoie un instantané complet à `/api/state`. Cette version enregistre cet instantané sur la base centrale, mais **ce n'est pas encore une synchronisation collaborative en temps réel robuste** : les modifications concurrentes peuvent s'écraser (dernier enregistrement gagnant), et les autres fenêtres ne sont pas automatiquement actualisées instantanément. Pour une utilisation multi-utilisateur intensive, il faudra remplacer ce stockage global par des opérations métier atomiques (entrée/sortie par ligne, transactions, journal append-only, contrôles de quantité) et ajouter une actualisation par polling ou WebSocket. Faites des sauvegardes régulières.

## Sécurité / exploitation
- Servez l'application uniquement en HTTPS en production.
- Utilisez un `SECRET_KEY` fort et un mot de passe administrateur unique.
- N'exposez pas directement le port PostgreSQL à Internet ; utilisez le réseau privé de l'hébergeur lorsque possible.
- Faites des sauvegardes PostgreSQL régulières et testez la restauration.
- La base SQLite de développement créée localement ne doit pas être utilisée comme base centrale de production.
