from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from database import get_supabase

router = APIRouter(prefix="/api/coach", tags=["Coach Financiero IA (Gemini)"])

class AskCoachRequest(BaseModel):
    pregunta: str

@router.post("/ask")
async def consultar_coach(req: AskCoachRequest):
    supabase = get_supabase()
    
    # 1. Obtener el usuario (para demo usamos el primero)
    users = supabase.table("usuarios").select("id, gemini_api_key").execute()
    if not users.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    user = users.data[0]
    api_key = user.get("gemini_api_key")
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key de Gemini no configurada. Ve a Configuración.")
        
    # 2. Recopilar contexto financiero para darle a la IA
    user_id = user["id"]
    
    ingresos = supabase.table("ingresos").select("*").eq("usuario_id", user_id).execute().data
    gastos_fijos = supabase.table("gastos_fijos").select("*").eq("usuario_id", user_id).execute().data
    tarjetas = supabase.table("tarjetas_credito").select("*").eq("usuario_id", user_id).execute().data
    prestamos = supabase.table("prestamos").select("*").eq("usuario_id", user_id).execute().data
    
    # Pre-procesar contexto
    total_ingresos = sum(i["monto"] for i in ingresos)
    total_fijos = sum(g["monto"] for g in gastos_fijos)
    total_deuda_mensual = sum(p["pago_mensual"] for p in prestamos)
    
    contexto_financiero = f"""
    Contexto Financiero Actual del Usuario:
    - Ingresos Totales (Fijos/Variables): ${total_ingresos:,.2f}
    - Obligaciones Mensuales Fijas: ${total_fijos:,.2f}
    - Pagos a Préstamos Mensuales: ${total_deuda_mensual:,.2f}
    - Tarjetas de Crédito Registradas: {len(tarjetas)}
    
    El usuario pregunta: "{req.pregunta}"
    """

    # 3. Llamar a Gemini API
    try:
        genai.configure(api_key=api_key)
        
        system_instruction = "Eres un Coach Financiero VIP, experto en finanzas personales, reducción de deudas y creación de riqueza. Analizas el contexto del usuario y das respuestas directas, profesionales, elegantes y accionables. No uses formato markdown de bloques de código en tus respuestas, habla natural pero estructurado."
        
        model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=system_instruction) # Usamos modelo pro o flash según preferencia
        
        response = model.generate_content(contexto_financiero)
        
        return {"respuesta": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando a Gemini: {str(e)}")

@router.post("/set-key")
async def configurar_api_key(api_key: str):
    supabase = get_supabase()
    users = supabase.table("usuarios").select("id").execute()
    if not users.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    user_id = users.data[0]["id"]
    
    try:
        supabase.table("usuarios").update({"gemini_api_key": api_key}).eq("id", user_id).execute()
        return {"msg": "API Key guardada exitosamente. Tu coach está listo."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
