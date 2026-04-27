from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI() # Fallo: Docs y Redoc habilitados por defecto (debería ser docs_url=None en prod)

# Fallo: CORS demasiado permisivo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS ---

class UserSchema(BaseModel):
    username: str
    password: str  # Fallo: El modelo de salida no debería incluir el password (PII Leak)
    email: str

# --- BASE DE DATOS (Simulada) ---

def get_db():
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()

# --- RUTAS ---

@app.post("/register", response_model=UserSchema)
async def register(user: UserSchema):
    # Aquí se devolvería el password en el JSON de respuesta por el response_model
    return user

@app.get("/search-users")
async def search_users(q: str, db: sqlite3.Connection = Depends(get_db)):
    # Fallo: Inyección SQL (Taint Flow: q -> query -> execute)
    query = f"SELECT username FROM users WHERE username LIKE '%{q}%'"
    cursor = db.execute(query)
    return cursor.fetchall()

@app.get("/admin/stats")
async def admin_stats():
    # Fallo: Ruta sensible sin dependencia de seguridad (Depends) o autenticación
    return {"status": "ok", "total_users": 1000, "system_load": "high"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
