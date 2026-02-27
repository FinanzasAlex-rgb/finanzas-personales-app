from fastapi import APIRouter, HTTPException
from typing import List
from database import get_supabase
from models import GastoPersonalCreate, GastoPersonalResponse

router = APIRouter(prefix="/api/gastos-personales", tags=["Gastos Personales (Variables)"])

@router.get("/", response_model=List[GastoPersonalResponse])
async def obtener_gastos_personales():
    supabase = get_supabase()
    try:
        response = supabase.table("gastos_personales").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=GastoPersonalResponse)
async def crear_gasto_personal(gasto: GastoPersonalCreate):
    supabase = get_supabase()
    
    users = supabase.table("usuarios").select("id").execute()
    user_id = users.data[0]["id"] if users.data else "00000000-0000-0000-0000-000000000000"

    data_insert = gasto.dict()
    data_insert["usuario_id"] = user_id
    
    try:
        response = supabase.table("gastos_personales").insert(data_insert).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
