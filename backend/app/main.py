"""
main.py - FastAPI entrypoint for AI Chatbot Backend
Versión: 0.1.0

Este archivo define el punto de entrada de la API REST del backend, usando FastAPI.
Incluye rutas para el widget del chatbot y la integración con Odoo y OpenAI.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .odoo_client import get_productos, get_inventario
from .ai_agent import run_crm_agent

app = FastAPI(
    title="AI Chatbot Backend",
    description="API modular para conectar el widget de chat con Odoo y OpenAI.",
    version="0.1.0"
)

# Modelos Pydantic para validación de datos
class HistoryEntry(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    history: Optional[List[HistoryEntry]] = []
    user_message: str

# Permitir CORS para el widget JS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    """Endpoint de prueba de vida"""
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    """Recibe mensajes del widget y responde usando OpenAI y Odoo"""
    # Construir el historial de conversación para el agente
    history_str = "\n".join([f"{entry.role}: {entry.content}" for entry in chat_request.history])
    history_str += f"\nuser: {chat_request.user_message}"

    # Llama al agente AI (OpenAI + Odoo)
    response = await run_crm_agent(history_context=history_str)
    return {"response": response}

@app.get("/productos")
def productos():
    """Devuelve productos de Odoo"""
    return get_productos()

@app.get("/inventario")
def inventario():
    """Devuelve inventario de Odoo"""
    return get_inventario()
