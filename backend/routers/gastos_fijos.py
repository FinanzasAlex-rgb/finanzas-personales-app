from fastapi import APIRouter, HTTPException
from typing import List
from database import get_supabase
from models import GastoFijoCreate, GastoFijoResponse

router = APIRouter(prefix="/api/gastos-fijos", tags=["Gastos Fijos"])

@router.get("/", response_model=List[GastoFijoResponse])
async def obtener_gastos_fijos():
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Error de conexión a BD")
    
    try:
        response = supabase.table("gastos_fijos").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=GastoFijoResponse)
async def crear_gasto_fijo(gasto: GastoFijoCreate):
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Error de conexión a BD")
    
    # Obtener un usuario base de prueba
    users = supabase.table("usuarios").select("id").execute()
    user_id = users.data[0]["id"] if users.data else "00000000-0000-0000-0000-000000000000"

    data_insert = gasto.dict()
    data_insert["usuario_id"] = user_id
    
    try:
        response = supabase.table("gastos_fijos").insert(data_insert).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{gasto_id}/estado")
async def actualizar_estado_gasto(gasto_id: str, nuevo_estado: str):
    supabase = get_supabase()
    if nuevo_estado not in ['pendiente', 'pagado', 'vencido']:
        raise HTTPException(status_code=400, detail="Estado inválido")
        
    try:
        response = supabase.table("gastos_fijos").update({"estado_actual": nuevo_estado}).eq("id", gasto_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{gasto_id}")
async def eliminar_gasto_fijo(gasto_id: str):
    supabase = get_supabase()
    try:
        response = supabase.table("gastos_fijos").delete().eq("id", gasto_id).execute()
        return {"msg": "Gasto fijo eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
