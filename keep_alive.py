import requests
import time
import os
from datetime import datetime

# URL de votre service Render (ex: https://votre-app.onrender.com)
# Vous pouvez aussi la mettre dans votre fichier .env sous RENDER_EXTERNAL_HOSTNAME
RENDER_URL = os.environ.get('RENDER_URL') or "https://backendimmo-o5r9.onrender.com/"
INTERVAL = 10 * 60  # 10 minutes en secondes

def keep_alive():
    if not RENDER_URL or "votre-app" in RENDER_URL:
        print("❌ Erreur : Veuillez configurer l'URL de votre service Render dans le script ou dans .env (variable RENDER_URL).")
        return

    print(f"--- Keep-Alive Script démarré pour {RENDER_URL} ---")
    print(f"Intervalle : {INTERVAL // 60} minutes")
    
    while True:
        try:
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] Ping vers {RENDER_URL}...", end=" ")
            
            # On fait un simple GET sur l'URL
            response = requests.get(RENDER_URL, timeout=30)
            
            if response.status_code == 200:
                print("✅ Succès (Code 200)")
            else:
                print(f"⚠️ Réponse avec code {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur lors du ping : {e}")
            
        # Attente avant le prochain ping
        time.sleep(INTERVAL)

if __name__ == "__main__":
    keep_alive()
