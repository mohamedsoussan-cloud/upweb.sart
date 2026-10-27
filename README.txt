The Printing Yassine — édition Client-Serveur

Lisez impérativement README_CENTRAL.md avant de déployer.

Cette édition est séparée en deux parties :
- app.py : serveur Flask central, authentification e-mail/mot de passe et base SQLAlchemy.
- desktop.py : client Windows qui ouvre le serveur distant configuré dans server_url.json.

Ne distribuez pas le dossier .venv ni les anciennes versions de dist. Compilez le client avec build_exe.bat après avoir configuré server_url.json.
