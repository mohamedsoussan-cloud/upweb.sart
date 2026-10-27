"""Importe l'ancien app_storage SQLite vers la base centrale DATABASE_URL.
À exécuter une seule fois, sur une copie de sauvegarde, avant l'ouverture aux utilisateurs.
"""
import os, sqlite3, sys
from sqlalchemy import text
from app import engine

source = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
    "The Printing Yassine", "printing_yassine_data.db")
if not os.path.isfile(source):
    raise SystemExit(f"Base SQLite introuvable : {source}\nIndiquez son chemin en argument.")
with sqlite3.connect(source) as old:
    try:
        rows = old.execute("SELECT key,value FROM app_storage WHERE key != '__data_version'").fetchall()
    except sqlite3.Error as exc:
        raise SystemExit(f"Ce fichier ne contient pas la table app_storage : {exc}")
with engine.begin() as conn:
    for key, value in rows:
        conn.execute(text("""INSERT INTO app_storage(key,value,updated_at) VALUES(:k,:v,CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value,updated_at=CURRENT_TIMESTAMP"""), {"k": key, "v": value})
print(f"Import terminé : {len(rows)} éléments importés depuis {source}")
print("Vérifiez les stocks sur le serveur avant de laisser plusieurs utilisateurs travailler.")
