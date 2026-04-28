from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

# 1. Instancia Hardened (Documentación oculta por defecto)
app = FastAPI(
    title="Secure FastAPI App",
    docs_url=None,   # Deshabilitar en producción
    redoc_url=None,
    openapi_url=None
)

# 2. Trusted Host Middleware (Prevenir ataques de cabecera Host)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["example.com", "*.example.com"]
)

# 3. CORS restringido (Nunca usar ["*"] en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/health")
async def health_check():
    return {"status": "secure"}
