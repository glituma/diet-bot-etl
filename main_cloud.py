import os
import requests

# GitHub ya tiene tu token guardado en secretos, así que lo usamos directo
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# 🔴 PEGA AQUÍ TU URL DE PIPEDREAM (Entre las comillas)
PIPEDREAM_URL = "https://eok4x4s0qhg6d5k.m.pipedream.net" 

def activar_puente():
    print(f"🌉 Conectando Bot con: {PIPEDREAM_URL}")
    
    # Armamos la URL de configuración
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={PIPEDREAM_URL}"
    
    try:
        # GitHub hace la petición por nosotros
        resp = requests.get(url, timeout=10)
        print("RESULTADO OFICIAL DE TELEGRAM:")
        print(resp.text)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    activar_puente()
