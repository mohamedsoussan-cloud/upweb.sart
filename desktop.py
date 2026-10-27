"""Client Windows : ouvre le serveur central dans une fenêtre desktop."""
import json
import os
import sys
from pathlib import Path
import webview

APP_NAME = "The Printing Yassine Desktop"

def app_dir():
    # For PyInstaller, keep config beside the executable, not inside _MEIPASS.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def server_url():
    value = os.environ.get("PRINTING_YASSINE_SERVER_URL", "").strip()
    config = app_dir() / "server_url.json"
    if not value and config.exists():
        try:
            value = str(json.loads(config.read_text(encoding="utf-8")).get("server_url", "")).strip()
        except Exception as exc:
            raise RuntimeError(f"Fichier server_url.json illisible : {exc}")
    if not value:
        raise RuntimeError("Configurez server_url.json avec l'URL HTTPS du serveur central. Voir README_CENTRAL.md.")
    if not value.startswith("https://") and not (value.startswith("http://127.0.0.1") or value.startswith("http://localhost")):
        raise RuntimeError("Pour un serveur distant, l'URL doit commencer par https://")
    return value.rstrip("/")

url = server_url()
webview.create_window(APP_NAME, url, width=1400, height=900, min_size=(1100, 700), resizable=True, confirm_close=True)
webview.start()
