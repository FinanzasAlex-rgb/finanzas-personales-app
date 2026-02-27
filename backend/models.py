from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# --- USUARIOS ---
class UsuarioCreate(BaseModel):
    correo: str
    gemini_api_key: Optional[str] = None
    tema_preferido: Optional[str] = "dark"

# --- INGRESOS ---
class IngresoBase(BaseModel):
    tipo: str # 'fijo' o 'variable'
    concepto: str
    monto: float
    frecuencia: Optional[str] = None
    fecha_ingreso: Optional[date] = None

class IngresoCreate(IngresoBase):
    pass

class IngresoResponse(IngresoBase):
    id: str
    usuario_id: str
    created_at: str

# --- GASTOS FIJOS ---
class GastoFijoBase(BaseModel):
    concepto: str
    monto: float
    dia_pago: int = Field(..., ge=1, le=31)
    estado_actual: Optional[str] = "pendiente"

class GastoFijoCreate(GastoFijoBase):
    pass

class GastoFijoResponse(GastoFijoBase):
    id: str
    usuario_id: str
    created_at: str

# --- TARJETAS DE CRÉDITO ---
class TarjetaCreditoBase(BaseModel):
    nombre_tarjeta: str
    limite_credito: float
    dia_corte: int = Field(..., ge=1, le=31)
    dia_pago: int = Field(..., ge=1, le=31)

class TarjetaCreditoCreate(TarjetaCreditoBase):
    pass

class TarjetaCreditoResponse(TarjetaCreditoBase):
    id: str
    usuario_id: str
    created_at: str

# --- PRÉSTAMOS ---
class PrestamoBase(BaseModel):
    entidad_otorgante: str
    monto_total: float
    pago_mensual: float
    fecha_inicio: date
    dia_pago: int = Field(..., ge=1, le=31)
    saldo_restante: float

class PrestamoCreate(PrestamoBase):
    pass

class PrestamoResponse(PrestamoBase):
    id: str
    usuario_id: str
    created_at: str

# --- GASTOS PERSONALES ---
class GastoPersonalBase(BaseModel):
    concepto: str
    monto: float
    categoria: str
    metodo_pago: str
    fecha_gasto: date

class GastoPersonalCreate(GastoPersonalBase):
    pass

class GastoPersonalResponse(GastoPersonalBase):
    id: str
    usuario_id: str
    created_at: str
