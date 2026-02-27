from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date, timedelta
from database import get_supabase
from models import TarjetaCreditoCreate, TarjetaCreditoResponse

router = APIRouter(prefix="/api/tarjetas", tags=["Tarjetas de Crédito y Amortizaciones"])

@router.get("/", response_model=List[TarjetaCreditoResponse])
async def obtener_tarjetas():
    supabase = get_supabase()
    try:
        response = supabase.table("tarjetas_credito").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=TarjetaCreditoResponse)
async def crear_tarjeta(tarjeta: TarjetaCreditoCreate):
    supabase = get_supabase()
    
    users = supabase.table("usuarios").select("id").execute()
    user_id = users.data[0]["id"] if users.data else "00000000-0000-0000-0000-000000000000"

    data_insert = tarjeta.dict()
    data_insert["usuario_id"] = user_id
    
    try:
        response = supabase.table("tarjetas_credito").insert(data_insert).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{tarjeta_id}/cargo")
async def registrar_cargo_tarjeta(tarjeta_id: str, monto: float, descripcion: str):
    supabase = get_supabase()
    
    try:
        # Obtener los datos de la tarjeta para calcular el pago
        tarjeta_res = supabase.table("tarjetas_credito").select("*").eq("id", tarjeta_id).execute()
        if not tarjeta_res.data:
            raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
            
        tarjeta = tarjeta_res.data[0]
        dia_corte = tarjeta["dia_corte"]
        dia_pago = tarjeta["dia_pago"]
        user_id = tarjeta["usuario_id"]
        
        # Guardar en gastos personales y cruzar
        gasto_insert = {
            "usuario_id": user_id,
            "concepto": descripcion,
            "monto": monto,
            "categoria": "Cargo a Tarjeta", # Se podría pedir por parámetro
            "metodo_pago": tarjeta_id,
            "fecha_gasto": str(date.today())
        }
        
        gasto_res = supabase.table("gastos_personales").insert(gasto_insert).execute()
        
        # Algoritmo de Amortización Tarjeta
        hoy = date.today()
        # Si hoy es <= que el día de corte dentro del mismo mes, se paga el día de pago del siguiente mes
        # Si hoy es > que el día de corte, el pago se va hasta el día de pago de DOS MESES en el futuro.
        # (Esto es una simplificación común para tarjetas mes-calendario).
        
        if hoy.day <= dia_corte:
            # Corte ya ha pasado en este mes para el registro anterior, pero para "hoy", el corte es *este* mes y se paga el mes que entra.
            mes_pago = hoy.month + 1 if hoy.month < 12 else 1
            anio_pago = hoy.year if hoy.month < 12 else hoy.year + 1
        else:
            # Pasó el corte, entra en el corte del próximo mes, pago en el siguiente del próximo
            mes_pago = hoy.month + 2
            anio_pago = hoy.year
            if mes_pago > 12:
                mes_pago -= 12
                anio_pago += 1
                
        fecha_pago_obj = date(anio_pago, mes_pago, dia_pago)
        
        # Amortización programada
        amortizacion_insert = {
            "usuario_id": user_id,
            "origen_tipo": "tarjeta_credito",
            "origen_id": tarjeta_id,
            "monto_pago": monto,
            "fecha_limite_pago": str(fecha_pago_obj),
            "estado": "pendiente"
        }
        
        supabase.table("pagos_amortizados").insert(amortizacion_insert).execute()
        
        return {"msg": f"Cargo de ${monto} registrado. Amortizado para pagar el {fecha_pago_obj}", "gasto": gasto_res.data[0]}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
