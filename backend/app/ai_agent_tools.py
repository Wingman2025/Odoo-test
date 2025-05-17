"""
ai_agent_tools.py - Herramientas function-calling para el agente AI (wingfoil)
Versión: 0.1.0

Define funciones que acceden a la API de Odoo para obtener información de productos e inventario,
y las registra como herramientas para el agente usando function_tool de openai-agents.
"""

from agents import function_tool
# from app.odoo_client import get_productos, get_inventario # Comentado para reemplazar
from .odoo_client import get_productos, get_inventario

@function_tool
def obtener_productos_odoo() -> list:
    """
    Devuelve una lista de los primeros 10 productos disponibles en la tienda Odoo.
    """
    return get_productos()

@function_tool
def obtener_inventario_odoo() -> list:
    """
    Devuelve una lista de los primeros 10 registros de inventario desde Odoo.
    """
    return get_inventario()
