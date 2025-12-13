import os
import requests
import urllib.parse
from datetime import date
from supabase import create_client, Client

# Recuperamos secretos del entorno (GitHub Secrets)
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
PHONE = os.environ.get("WHATSAPP_PHONE")
API_KEY = os.environ.get("WHATSAPP_API_KEY")

supabase: Client = create_client(URL, KEY)

def enviar_whatsapp_api(mensaje):
    """Envía mensaje usando CallMeBot API (Funciona en Servidores)"""
    print("📤 Enviando a WhatsApp API...")
    msg_encoded = urllib.parse.quote(mensaje)
    url = f"https://api.callmebot.com/whatsapp.php?phone={PHONE}&text={msg_encoded}&apikey={API_KEY}"
    
    try:
        resp = requests.get(url, timeout=20) # Timeout largo por seguridad
        if resp.status_code == 200:
            print("✅ Mensaje entregado exitosamente.")
        else:
            print(f"❌ Error API: {resp.status_code} - {resp.text}")
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
    
    # Usamos formato simple para asegurar compatibilidad
    mensaje = (
        f"📅 *PLAN GORKI - {hoy}*\n"
        f"🎯 {plan.get('meta')}\n\n"
        f"🍳 *Desayuno:* {c.get('desayuno')}\n"
        f"🥗 *Almuerzo:* {c.get('almuerzo')}\n"
        f"🍎 *Media Tarde:* {c.get('merienda')}\n\n"
        f"💪 *Entrenamiento:* {plan.get('entrenamiento')}"
    )
    
    # 3. Enviar
    enviar_whatsapp_api(mensaje)

if __name__ == "__main__":
    main()