from fastapi import APIRouter, HTTPException, Depends
from typing import List
from database import get_supabase
from models import IngresoCreate, IngresoResponse

router = APIRouter(prefix="/api/ingresos", tags=["Ingresos"])

# Mock User ID para la fase inicial (luego se integrará auth)
# En una app real, esto vendría del token JWT de la sesión.
MOCK_USER_ID = "00000000-0000-0000-0000-000000000000"

@router.get("/", response_model=List[IngresoResponse])
async def obtener_ingresos():
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Error de conexión a BD")
    
    # Intenta obtener el mock user (crearlo si no existe para flujos locales rápidos)
    try:
        response = supabase.table("ingresos").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=IngresoResponse)
async def crear_ingreso(ingreso: IngresoCreate):
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Error de conexión a BD")
    
    # Asegurar que haya un usuario (solo para demo local/fase dev)
    users = supabase.table("usuarios").select("id").execute()
    if not users.data:
        new_user = supabase.table("usuarios").insert({"correo": "admin@finanzas.vip"}).execute()
        user_id = new_user.data[0]["id"]
    else:
        user_id = users.data[0]["id"]

    data_insert = ingreso.dict()
    data_insert["usuario_id"] = user_id
    
    try:
        response = supabase.table("ingresos").insert(data_insert).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{ingreso_id}")
async def eliminar_ingreso(ingreso_id: str):
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(status_code=500, detail="Error de conexión a BD")
    
    try:
        response = supabase.table("ingresos").delete().eq("id", ingreso_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Ingreso no encontrado")
        return {"msg": "Ingreso eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
