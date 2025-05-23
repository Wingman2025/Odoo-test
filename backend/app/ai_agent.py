"""
ai_agent.py - Agente CRM modular para FastAPI
Versión: 0.4.0

Este módulo define los agentes usando openai-agents, siguiendo las mejores prácticas de modularidad y comentarios profesionales.
Incluye guardrails para detección de lenguaje inapropiado.
"""

from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Runner, GuardrailFunctionOutput, input_guardrail, InputGuardrailTripwireTriggered
import os
from typing import Union, List, Dict, Any

# --- Cargar variables de entorno (.env) ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --- Crear cliente OpenAI ---
openai_client = OpenAI(api_key=api_key)

# --- Guardrail para lenguaje inapropiado usando un agente guardrail (OpenAI Agents SDK) ---
from pydantic import BaseModel
from agents import Runner, RunContextWrapper, TResponseInputItem

class ProfanityGuardrailOutput(BaseModel):
    is_inappropriate: bool
    reasoning: str

profanity_guardrail_agent = Agent(
    name="Profanity Guardrail Agent",
    instructions="Detecta si el mensaje contiene lenguaje como gay, lesbiano, homosexuales, transexuales, ofensivo o tóxico. Devuelve is_inappropriate=True si lo detectas y explica por qué en 'reasoning'.",
    output_type=ProfanityGuardrailOutput,
    model="gpt-4o"
)

@input_guardrail
async def profanity_guardrail(ctx: RunContextWrapper[None], agent: Agent, user_input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    """
    Guardrail que utiliza un agente LLM para detectar lenguaje inapropiado.
    Dispara un tripwire si se detecta contenido inapropiado.
    """
    result = await Runner.run(profanity_guardrail_agent, user_input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_inappropriate
    )


# --- Definir el agente CRM, instrucciones consultivas y breves ---
from .ai_agent_tools import (
    obtener_productos_odoo,
    obtener_inventario_odoo,
    obtener_pedidos_compra_odoo,
    obtener_pedidos_compra_detallado_odoo,
    obtener_lineas_pedido_odoo
)

crm_agent = Agent(
    name="crm_agent",
    instructions="""
Eres un agente comercial experto en deportes acuáticos, especializado en wingfoil y kitesurf, tu misión principal es vender los productos de nuestra tienda online. Tienes acceso a información actualizada de productos, stock y precios a través de las APIs de Odoo.

- Atiendes a los clientes con un tono profesional, cercano y entusiasta, mostrando pasión por el wingfoil y conocimiento técnico real de los productos.
- Tu objetivo es asesorar, resolver dudas y guiar a los clientes para que encuentren el equipo de wingfoil ideal según su nivel, necesidades y presupuesto.
- Si el cleinte pregunta por productos de una forma general, no es necesario mostrar el listado total de productos disponibles en la tienda, pero si es bueno explicar que hay diferentes modelos para que e cliente tenga una vision global de los productos disponibles y Haz preguntas para entender mejor las necesidades del cliente antes de recomendar productos especificos.
- Responde de forma consultiva, breve y clara. 
- Siempre que sea relevante, sugiere productos concretos de nuestro catálogo, destacando ventajas, características técnicas, diferencias entre modelos.
- Si el cliente busca algo específico (ejemplo: "alas para principiantes", "tablas avanzadas", "ofertas en stock"), filtra y recomienda productos relevantes usando la información de la tienda a traves de las apis de odoo.
- Si el cliente solicita contacto humano, ofrécele el enlace directo a WhatsApp: https://wa.me/34657362988?text=Hola%20quiero%20más%20info%20sobre%20productos%20wingfoil

Nunca inventes información sobre productos que no existen en la tienda. Si no tienes datos suficientes, pide detalles o sugiere consultar con un asesor humano.
""",
    model="gpt-4o",
    tools=[obtener_productos_odoo, obtener_inventario_odoo],
    input_guardrails=[profanity_guardrail]
)


# --- Instanciar el runner para el agente ---
runner = Runner()

# --- Función asíncrona para invocar el agente CRM ---
async def run_crm_agent(history_context: str) -> str:
    """
    Ejecuta el agente CRM con el historial de conversación como contexto.
    Devuelve la respuesta generada por el agente.
    """
    try:
        response = await runner.run(crm_agent, input=history_context)
        return response.final_output
    except InputGuardrailTripwireTriggered:
        # Respuesta personalizada cuando se detecta lenguaje inapropiado
        return (
            "Lo siento, tu mensaje contiene lenguaje inapropiado "
            "y no puedo procesarlo. 🙏 Por favor, mantén un tono respetuoso."
        )
    except Exception as e:
        return f"[Error AI]: {str(e)}"

# -----------------------------------------------------------------------------
# Agente de Gestión Interna (Stock y Pedidos)
# -----------------------------------------------------------------------------
# Este agente está especializado en la gestión interna de stock y pedidos,
# accediendo a la información de inventario y productos vía Odoo.
# Su objetivo es resolver consultas internas sobre existencias, movimientos y pedidos,
# y puede ser utilizado por personal interno o agentes automatizados.
# -----------------------------------------------------------------------------

internal_ops_agent = Agent(
    name="internal_ops_agent",
    handoff_description="Agente especializado en gestión interna de stock y pedidos (Odoo)",
    instructions="""
Eres un agente de gestión interna para una tienda de deportes acuáticos. Tu función es responder consultas sobre stock, inventario y pedidos. Utiliza las APIs de Odoo para obtener información precisa y actualizada. Responde de forma clara, profesional y orientada a la acción.

- Puedes informar sobre niveles de stock, disponibilidad de productos, movimientos de inventario y estados de pedidos.
- Si una consulta requiere intervención humana, indícalo claramente.
- Nunca inventes datos: si la información no está disponible, solicita detalles adicionales o indica la falta de datos.
- Utiliza las herramientas disponibles para consultar inventario y productos.
- Responde siempre con precisión y brevedad, orientado a resolver la gestión interna.
""",
    model="gpt-4o",
    tools=[
        obtener_productos_odoo,
        obtener_inventario_odoo,
        obtener_pedidos_compra_odoo,
        obtener_pedidos_compra_detallado_odoo,
        obtener_lineas_pedido_odoo
    ],
    input_guardrails=[profanity_guardrail]
)

async def run_internal_ops_agent(history_context: str) -> str:
    """
    Ejecuta el agente de gestión interna con el historial de conversación como contexto.
    Devuelve la respuesta generada por el agente.
    """
    try:
        response = await runner.run(internal_ops_agent, input=history_context)
        return response.final_output
    except InputGuardrailTripwireTriggered:
        # Respuesta personalizada cuando se detecta lenguaje inapropiado
        return (
            "Lo siento, tu mensaje contiene lenguaje inapropiado "
            "y no puedo procesarlo. 🙏 Por favor, mantén un tono respetuoso."
        )
    except Exception as e:
        return f"[Error AI]: {str(e)}"

# -----------------------------------------------------------------------------
# Triage Agent para Gestión Interna
# -----------------------------------------------------------------------------
# Este agente actúa como filtro inteligente (triage) para derivar consultas
# relacionadas con gestión interna (stock/pedidos) al agente adecuado.
# Puede identificar si una consulta es operativa/interna o comercial/cliente
# y redirigirla al agente correspondiente.
# -----------------------------------------------------------------------------

triage_agent = Agent(
    name="triage_agent",
    instructions="""
eres un agente de triage. tu tarea es derivar las consultas al agente adecuado.
despues de saludar, Pregunta si quiere ser atendido por un agente comercial y si es asi deriva al agente "crm_agent". o si quiere ser atendido por una gente adminstrativo y deriva al agente "internal_ops_agent". 
si las preguntas son comerciales, de ventas o atención al cliente, deriva al agente "crm_agent".
Si las preguntas son sobre stock, inventario, almacén o pedidos, deriva al agente "internal_ops_agent".
""",
    handoffs=[internal_ops_agent, crm_agent],
    model="gpt-4o"
)

async def run_triage_agent(
    history_context: str,
    workflow_name: str = "chat_with_triage",
    trace_id: str = None,
    group_id: str = None,
    trace_metadata: dict = None
) -> str:
    """
    Ejecuta el triage agent para decidir a qué agente (CRM o gestión interna) debe ser derivada la consulta.
    Toda la orquestación, handoff y manejo de errores se realiza aquí.

    Parámetros:
        history_context (str): Historial de la conversación en formato string.
        workflow_name (str, opcional): Nombre lógico del flujo para trazabilidad y auditoría. Default: "chat_with_triage".
        trace_id (str, opcional): Identificador único de la traza. Si no se proporciona, se genera automáticamente.
        group_id (str, opcional): Identificador de grupo para agrupar varias trazas (por ejemplo, por sesión de chat).
        trace_metadata (dict, opcional): Diccionario con metadata adicional relevante para auditoría (ej: user_id, motivo, etc).

    Returns:
        str: Respuesta final generada por el agente adecuado, o mensaje de error.

    Ejemplo de uso:
        response = await run_triage_agent(
            history_context,
            workflow_name="gestion_stock",
            trace_id="trace_1234567890abcdef",
            group_id="chat_session_001",
            trace_metadata={"user_id": "42", "agent_entry": "triage_agent"}
        )
    """
    try:
        from agents import RunConfig
        run_config = RunConfig(
            workflow_name=workflow_name,
            trace_id=trace_id,
            group_id=group_id,
            trace_metadata=trace_metadata
        )

        response = await runner.run(
            triage_agent,
            input=history_context,
            run_config=run_config
        )
        return response.final_output
    except InputGuardrailTripwireTriggered:
        # Respuesta personalizada cuando se detecta lenguaje inapropiado
        return (
            "Lo siento, tu mensaje contiene lenguaje inapropiado "
            "y no puedo procesarlo. 🙏 Por favor, mantén un tono respetuoso."
        )
    except Exception as e:
        return f"[Error AI]: {str(e)}"
