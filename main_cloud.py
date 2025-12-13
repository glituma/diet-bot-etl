import os
import requests
from datetime import date
from supabase import create_client, Client

# Secretos
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
TG_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

supabase: Client = create_client(URL, KEY)

def enviar_telegram(mensaje):
    print("📤 Enviando a Telegram...")
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
        print("✅ Mensaje entregado.")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    hoy = str(date.today())
    print(f"🤖 Ejecutando ETL Cloud para: {hoy}")
    
    # 1. Consultar BD
    data = supabase.table("diet_plans").select("content").eq("date_assigned", hoy).execute()
    
    if not data.data:
        print("⚠️ No hay plan para hoy.")
        return

    # 2. Formatear Mensaje "Premium"
    plan = data.data[0]['content']
    c = plan.get('comidas', {})
    extras = plan.get('extras', 'Hidratación y descanso')

    # Diseño visual con separadores y emojis
    mensaje = (
        f"📅 *PLAN GORKI - {hoy}*\n"
        f"🎯 _{plan.get('meta')}_\n"
        f"➖➖➖➖➖➖➖➖➖➖\n"
        f"🍳 *DESAYUNO*\n"
        f"{c.get('desayuno')}\n\n"
        f"🥗 *ALMUERZO*\n"
        f"{c.get('almuerzo')}\n\n"
        f"🍎 *SNACK / CENA*\n"
        f"{c.get('merienda')}\n"
        f"➖➖➖➖➖➖➖➖➖➖\n"
        f"💪 *ENTRENAMIENTO*\n"
        f"{plan.get('entrenamiento')}\n\n"
        f"💧 *RECORDATORIOS*\n"
        f"{extras}"
    )
    
    # 3. Enviar
    enviar_telegram(mensaje)

if __name__ == "__main__":
    main()
