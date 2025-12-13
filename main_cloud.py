import os
import requests
from datetime import date
from supabase import create_client, Client

# Secretos de GitHub
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
TG_TOKEN = os.environ.get("TELEGRAM_TOKEN")   # Nuevo
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID") # Nuevo

supabase: Client = create_client(URL, KEY)

def enviar_telegram(mensaje):
    """Envía mensaje oficial a Telegram"""
    print("📤 Enviando a Telegram...")
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown" # Para usar negritas con *texto*
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            print("✅ Mensaje entregado en Telegram.")
        else:
            print(f"❌ Error Telegram: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def main():
    hoy = str(date.today())
    print(f"🤖 Ejecutando ETL Cloud para: {hoy}")
    
    # 1. Consultar Base de Datos
    data = supabase.table("diet_plans").select("content").eq("date_assigned", hoy).execute()
    
    if not data.data:
        print(f"⚠️ No hay dieta para hoy ({hoy}).")
        return

    # 2. Formatear Mensaje
    plan = data.data[0]['content']
    c = plan.get('comidas', {})
    
    # Formato Markdown para Telegram
    mensaje = (
        f"📅 *PLAN GORKI - {hoy}*\n"
        f"🎯 _{plan.get('meta')}_\n\n"
        f"🍳 *Desayuno:* {c.get('desayuno')}\n"
        f"🥗 *Almuerzo:* {c.get('almuerzo')}\n"
        f"🍎 *Media Tarde:* {c.get('merienda')}\n\n"
        f"💪 *Entrenamiento:* {plan.get('entrenamiento')}"
    )
    
    # 3. Enviar
    enviar_telegram(mensaje)

if __name__ == "__main__":
    main()
