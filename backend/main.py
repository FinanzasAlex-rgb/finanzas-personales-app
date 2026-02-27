from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from routers import ingresos, gastos_fijos, prestamos, tarjetas, gastos_personales, coach

app = FastAPI(title="Finanzas Personales API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Mount static files (frontend)
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")
app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/sw.js")
async def serve_sw():
    return FileResponse(os.path.join(FRONTEND_DIR, "sw.js"))

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "app": "Finanzas Personales API"}

# Include routers
app.include_router(ingresos.router)
app.include_router(gastos_fijos.router)
app.include_router(prestamos.router)
app.include_router(tarjetas.router)
app.include_router(gastos_personales.router)
app.include_router(coach.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
