"""Créer un compte depuis le terminal du serveur : python create_user.py"""
import getpass
import re
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from app import engine

email = input("E-mail du nouvel utilisateur : ").strip().lower()
password = getpass.getpass("Mot de passe (12 caractères minimum) : ")
role = (input("Rôle [user/admin] (user) : ").strip().lower() or "user")
if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
    raise SystemExit("Adresse e-mail invalide.")
if len(password) < 12:
    raise SystemExit("Le mot de passe doit contenir au moins 12 caractères.")
if role not in ("user", "admin"):
    raise SystemExit("Le rôle doit être user ou admin.")
try:
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO users(email,password_hash,role) VALUES(:e,:p,:r)"), {
            "e": email, "p": generate_password_hash(password), "r": role
        })
    print(f"Compte créé : {email} ({role})")
except Exception as exc:
    raise SystemExit(f"Impossible de créer le compte (e-mail peut-être déjà utilisé) : {exc}")
