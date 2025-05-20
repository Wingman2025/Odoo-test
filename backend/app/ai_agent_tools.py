"""
ai_agent_tools.py - Herramientas function-calling para el agente AI (wingfoil)
Versión: 0.1.0

Define funciones que acceden a la API de Odoo para obtener información de productos e inventario,
y las registra como herramientas para el agente usando function_tool de openai-agents.
"""

from agents import function_tool
from .odoo_client import (
    get_productos, get_inventario, get_pedidos_compra, 
    get_pedidos_compra_detallado, get_lineas_pedido
)

@function_tool
def obtener_productos_odoo() -> list:
    """Devuelve los primeros 10 productos de Odoo."""
    return get_productos()

@function_tool
def obtener_inventario_odoo() -> list:
    """Devuelve los primeros 10 registros de inventario."""
    return get_inventario()

@function_tool
def obtener_pedidos_compra_odoo() -> list:
    """Devuelve los primeros 10 pedidos de compra."""
    return get_pedidos_compra()

@function_tool
def obtener_pedidos_compra_detallado_odoo() -> list:
    """Devuelve los primeros 10 pedidos con sus líneas."""
    return get_pedidos_compra_detallado()

@function_tool
def obtener_lineas_pedido_odoo(order_id: int) -> list:
    """
    Devuelve las líneas de un pedido de compra específico.
    
    Parámetros:
        order_id: ID del pedido de compra.
    """
    return get_lineas_pedido(order_id)
