-- 1. Tabla de Usuarios / Settings Generales
CREATE TABLE IF NOT EXISTS public.usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    correo VARCHAR UNIQUE NOT NULL,
    gemini_api_key TEXT, -- Se debe guardar de forma segura (idealmente encriptado si se requiere)
    tema_preferido VARCHAR DEFAULT 'dark',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Tabla de Ingresos (Fijos y Variables)
CREATE TABLE IF NOT EXISTS public.ingresos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES public.usuarios(id) ON DELETE CASCADE,
    tipo VARCHAR NOT NULL CHECK (tipo IN ('fijo', 'variable')),
    concepto VARCHAR NOT NULL,
    monto DECIMAL(12,2) NOT NULL,
    frecuencia VARCHAR, -- Ej. 'quincenal', 'mensual' (solo para fijos)
    fecha_ingreso DATE, -- Cuando es variable, o la primera fecha del fijo
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Tabla de Gastos Fijos (Servicios, Rentas)
CREATE TABLE IF NOT EXISTS public.gastos_fijos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES public.usuarios(id) ON DELETE CASCADE,
    concepto VARCHAR NOT NULL,
    monto DECIMAL(12,2) NOT NULL,
    dia_pago INTEGER NOT NULL CHECK (dia_pago >= 1 AND dia_pago <= 31),
    estado_actual VARCHAR DEFAULT 'pendiente' CHECK (estado_actual IN ('pendiente', 'pagado', 'vencido')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Tabla de Tarjetas de Crédito
CREATE TABLE IF NOT EXISTS public.tarjetas_credito (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES public.usuarios(id) ON DELETE CASCADE,
    nombre_tarjeta VARCHAR NOT NULL,
    limite_credito DECIMAL(12,2),
    dia_corte INTEGER NOT NULL CHECK (dia_corte >= 1 AND dia_corte <= 31),
    dia_pago INTEGER NOT NULL CHECK (dia_pago >= 1 AND dia_pago <= 31),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Tabla de Préstamos
CREATE TABLE IF NOT EXISTS public.prestamos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES public.usuarios(id) ON DELETE CASCADE,
    entidad_otorgante VARCHAR NOT NULL,
    monto_total DECIMAL(12,2) NOT NULL,
    pago_mensual DECIMAL(12,2) NOT NULL,
    fecha_inicio DATE NOT NULL,
    dia_pago INTEGER NOT NULL CHECK (dia_pago >= 1 AND dia_pago <= 31),
    saldo_restante DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Tabla de Gastos Personales Variables (Comida, Salidas, etc)
CREATE TABLE IF NOT EXISTS public.gastos_personales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES public.usuarios(id) ON DELETE CASCADE,
    concepto VARCHAR NOT NULL,
    monto DECIMAL(12,2) NOT NULL,
    categoria VARCHAR NOT NULL, -- 'comida', 'alcohol', 'botana', 'salida_amigos', 'hijo', etc.
    metodo_pago VARCHAR NOT NULL, -- 'efectivo', 'debito', o el ID de la tarjeta de credito
    fecha_gasto DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. Tabla de Amortizaciones (Pagos proyectados programados para deudas/tarjetas)
CREATE TABLE IF NOT EXISTS public.pagos_amortizados (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES public.usuarios(id) ON DELETE CASCADE,
    origen_tipo VARCHAR NOT NULL CHECK (origen_tipo IN ('tarjeta_credito', 'prestamo')),
    origen_id UUID NOT NULL, -- Puede apuntar a tarjeta_credito(id) o prestamos(id)
    monto_pago DECIMAL(12,2) NOT NULL,
    fecha_limite_pago DATE NOT NULL,
    estado VARCHAR DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'pagado', 'vencido')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ACTIVAR ROW LEVEL SECURITY (Opcional pero muy recomendado para producción)
-- Aquí damos acceso a todo por ahora asumiendo que el control de acceso inicial se hará por backend
ALTER TABLE public.usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ingresos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gastos_fijos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tarjetas_credito ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.prestamos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gastos_personales ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pagos_amortizados ENABLE ROW LEVEL SECURITY;

-- Políticas permisivas (ajustar en producción usando supabase.auth.uid())
CREATE POLICY "Permitir todo temporal" ON public.usuarios FOR ALL USING (true);
CREATE POLICY "Permitir todo temporal" ON public.ingresos FOR ALL USING (true);
CREATE POLICY "Permitir todo temporal" ON public.gastos_fijos FOR ALL USING (true);
CREATE POLICY "Permitir todo temporal" ON public.tarjetas_credito FOR ALL USING (true);
CREATE POLICY "Permitir todo temporal" ON public.prestamos FOR ALL USING (true);
CREATE POLICY "Permitir todo temporal" ON public.gastos_personales FOR ALL USING (true);
CREATE POLICY "Permitir todo temporal" ON public.pagos_amortizados FOR ALL USING (true);
