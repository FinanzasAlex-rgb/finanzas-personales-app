from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date, timedelta
from database import get_supabase
from models import PrestamoCreate, PrestamoResponse

router = APIRouter(prefix="/api/prestamos", tags=["Prestamos y Amortizaciones"])

@router.get("/", response_model=List[PrestamoResponse])
async def obtener_prestamos():
    supabase = get_supabase()
    try:
        response = supabase.table("prestamos").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=PrestamoResponse)
async def crear_prestamo(prestamo: PrestamoCreate):
    supabase = get_supabase()
    
    # Usuario por defecto para demo
    users = supabase.table("usuarios").select("id").execute()
    user_id = users.data[0]["id"] if users.data else "00000000-0000-0000-0000-000000000000"

    data_insert = prestamo.dict()
    data_insert["usuario_id"] = user_id
    
    try:
        # 1. Crear el préstamo base
        response = supabase.table("prestamos").insert(data_insert).execute()
        nuevo_prestamo = response.data[0]
        prestamo_id = nuevo_prestamo["id"]
        
        # 2. LÓGICA DE AMORTIZACIÓN AUTOMÁTICA
        # Calcula cuántos meses tardará en pagar
        monto_total = prestamo.monto_total
        pago_mensual = prestamo.pago_mensual
        dia_pago = prestamo.dia_pago
        fecha_actual = prestamo.fecha_inicio
        
        meses_estimados = int(monto_total // pago_mensual)
        residuo = monto_total % pago_mensual
        
        amortizaciones = []
        fecha_iteracion = prestamo.fecha_inicio
        
        # Ajustamos el primer mes para que coincida con el día de pago pactado
        if fecha_iteracion.day > dia_pago:
             # Si ya pasó el día de pago en el mes actual, se cobra el mes siguiente
             mes_cobro = fecha_iteracion.month + 1 if fecha_iteracion.month < 12 else 1
             anio_cobro = fecha_iteracion.year if fecha_iteracion.month < 12 else fecha_iteracion.year + 1
        else:
             mes_cobro = fecha_iteracion.month
             anio_cobro = fecha_iteracion.year
             
        # Crear los pagos completos
        for i in range(meses_estimados):
            fecha_pago_obj = date(anio_cobro, mes_cobro, dia_pago)
            amortizaciones.append({
                "usuario_id": user_id,
                "origen_tipo": "prestamo",
                "origen_id": prestamo_id,
                "monto_pago": pago_mensual,
                "fecha_limite_pago": str(fecha_pago_obj),
                "estado": "pendiente"
            })
            
            # Avanzar un mes
            mes_cobro += 1
            if mes_cobro > 12:
                mes_cobro = 1
                anio_cobro += 1
                
        # Crear pago para el residuo si lo hay
        if residuo > 0:
            fecha_pago_obj = date(anio_cobro, mes_cobro, dia_pago)
            amortizaciones.append({
                "usuario_id": user_id,
                "origen_tipo": "prestamo",
                "origen_id": prestamo_id,
                "monto_pago": residuo,
                "fecha_limite_pago": str(fecha_pago_obj),
                "estado": "pendiente"
            })
            
        # 3. Guardar las amortizaciones en Supabase en Batch
        if amortizaciones:
            supabase.table("pagos_amortizados").insert(amortizaciones).execute()
            
        return nuevo_prestamo
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
