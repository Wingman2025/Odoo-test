"""
main.py - FastAPI entrypoint for AI Chatbot Backend
Versión: 0.1.0

Este archivo define el punto de entrada de la API REST del backend, usando FastAPI.
Incluye rutas para el widget del chatbot y la integración con Odoo y OpenAI.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any
from agents import InputGuardrailTripwireTriggered  # Importar la excepción del guardrail
from .odoo_client import (
    get_productos, get_inventario, get_pedidos_compra, get_pedidos_compra_detallado, get_lineas_pedido
)
from .ai_agent import run_crm_agent, run_triage_agent

app = FastAPI(
    title="AI Chatbot Backend",
    description="API modular para conectar el widget de chat con Odoo y OpenAI.",
    version="0.1.0"
)

# Modelos Pydantic para validación de datos
class HistoryEntry(BaseModel):
    role: str  # 'user' o 'assistant'. Indica quién envió el mensaje.
    content: str  # Texto del mensaje.

    class Config:
        schema_extra = {
            "example": {
                "role": "user",
                "content": "Hola, ¿qué productos tenéis en stock?"
            }
        }

class ChatRequest(BaseModel):
    """
    Modelo de entrada para el endpoint /chat.
    Incluye el historial de la conversación (lista de mensajes previos, cada uno con rol y contenido) y el mensaje actual del usuario.
    Este modelo permite que el agente AI tenga contexto completo para tomar decisiones y generar respuestas precisas.
    """
    history: Optional[List[HistoryEntry]] = []  # Historial previo de la conversación.
    user_message: str  # Mensaje actual del usuario.

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
    """
    Endpoint de prueba de vida (health check).
    Permite comprobar que el backend está corriendo correctamente.
    Útil para monitoreo y despliegue en Railway u otros servicios.

    Returns:
        dict: {"status": "ok"} si el backend está activo.
    """
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    """
    Endpoint principal de chat conversacional.

    Descripción:
    - Recibe el historial de la conversación y el mensaje actual del usuario.
    - Invoca el triage agent, que automáticamente analiza el mensaje y, gracias al sistema de handoffs de openai-agents, deriva internamente la consulta al agente más adecuado (CRM o gestión interna) según el contexto y el contenido.
    - El backend no realiza lógica de selección manual; simplemente retorna la respuesta final generada por el agente correspondiente.

    Este flujo garantiza modularidad, mantenibilidad y máxima integración con la arquitectura de agentes AI.

    Returns:
        dict: {"response": respuesta generada por el agente adecuado}
    """
    try:
        # Construir historial de conversación
        history_str = "\n".join([f"{entry.role}: {entry.content}" for entry in chat_request.history])
        history_str += f"\nuser: {chat_request.user_message}"

        # Invocar la función centralizada de agentes (manejo de handoff y errores en ai_agent.py)
        from .ai_agent import run_triage_agent
        response = await run_triage_agent(history_str)
        return {"response": response}
        
    except InputGuardrailTripwireTriggered:
        # Manejar lenguaje inapropiado detectado por el guardrail
        return {
            "response": "Lo siento, no puedo procesar mensajes con lenguaje inapropiado. " \
                       "Por favor, reformula tu consulta de manera respetuosa."
        }
    except Exception as e:
        # Manejar otros errores inesperados
        return {
            "response": f"Lo siento, ha ocurrido un error al procesar tu mensaje. {str(e)}"
        }


from fastapi import Query
import json

@app.get("/productos")
def productos(domain: str = Query(None, description="Filtro Odoo en formato JSON"), limit: int = Query(None, description="Máximo de productos a devolver")):
    """
    Devuelve productos de Odoo según filtros y límite opcionales.
    Permite filtrar y limitar resultados vía query params.
    Ejemplo: /productos?domain=[["type","=","consu"]]&limit=5
    """
    parsed_domain = json.loads(domain) if domain else None
    return get_productos(domain=parsed_domain, limit=limit)

@app.get("/inventario")
def inventario(domain: str = Query(None, description="Filtro Odoo en formato JSON"), limit: int = Query(None, description="Máximo de registros a devolver")):
    """
    Devuelve registros de inventario según filtros y límite opcionales.
    Ejemplo: /inventario?domain=[["product_id","=",123]]&limit=10
    """
    parsed_domain = json.loads(domain) if domain else None
    return get_inventario(domain=parsed_domain, limit=limit)

@app.get("/pedidos_compra")
def pedidos_compra(domain: str = Query(None, description="Filtro Odoo en formato JSON"), limit: int = Query(None, description="Máximo de pedidos a devolver")):
    """
    Devuelve pedidos de compra según filtros y límite opcionales.
    Ejemplo: /pedidos_compra?domain=[["state","=","purchase"]]&limit=5
    """
    parsed_domain = json.loads(domain) if domain else None
    return get_pedidos_compra(domain=parsed_domain, limit=limit)

@app.get("/pedidos_compra_detallado")
def pedidos_compra_detallado(domain: str = Query(None, description="Filtro Odoo en formato JSON"), limit: int = Query(None, description="Máximo de pedidos a devolver")):
    """
    Devuelve pedidos de compra con líneas anidadas, según filtros y límite opcionales.
    Ejemplo: /pedidos_compra_detallado?limit=3
    """
    parsed_domain = json.loads(domain) if domain else None
    return get_pedidos_compra_detallado(domain=parsed_domain, limit=limit)

@app.get("/lineas_pedido/{order_id}")
def lineas_pedido(order_id: int):
    """
    Devuelve las líneas de un pedido de compra específico.
    Ejemplo: /lineas_pedido/123
    """
    return get_lineas_pedido(order_id)
