"""
ai_agent_tools.py - Herramientas function-calling para el agente AI (wingfoil)
Versión: 0.1.0

Define funciones que acceden a la API de Odoo para obtener información de productos e inventario,
y las registra como herramientas para el agente usando function_tool de openai-agents.
"""

from agents import function_tool
# from app.odoo_client import get_productos, get_inventario # Comentado para reemplazar
from .odoo_client import (
    get_productos, get_inventario, get_pedidos_compra, get_pedidos_compra_detallado, get_lineas_pedido
)

@function_tool
def obtener_productos_odoo(domain: list = None, limit: int = None) -> list:
    """
    Devuelve productos de Odoo según filtros y límite opcionales.
    Parámetros:
        domain (list, opcional): Filtros de búsqueda Odoo (por ejemplo: [["type", "=", "consu"]]).
        limit (int, opcional): Máximo de productos a devolver.
    """
    return get_productos(domain=domain, limit=limit)

@function_tool
def obtener_inventario_odoo(domain: list = None, limit: int = None) -> list:
    """
    Devuelve registros de inventario de Odoo según filtros y límite opcionales.
    Parámetros:
        domain (list, opcional): Filtros de búsqueda Odoo (por ejemplo: [["product_id", "=", 123]]).
        limit (int, opcional): Máximo de registros a devolver.
    """
    return get_inventario(domain=domain, limit=limit)

@function_tool
def obtener_pedidos_compra_odoo(domain: list = None, limit: int = None) -> list:
    """
    Devuelve pedidos de compra de Odoo según filtros y límite opcionales.
    Parámetros:
        domain (list, opcional): Filtros de búsqueda Odoo (por ejemplo: [["state", "=", "purchase"]]).
        limit (int, opcional): Máximo de pedidos a devolver.
    """
    return get_pedidos_compra(domain=domain, limit=limit)

@function_tool
def obtener_pedidos_compra_detallado_odoo(domain: list = None, limit: int = None) -> list:
    """
    Devuelve pedidos de compra con líneas anidadas, según filtros y límite opcionales.
    Parámetros:
        domain (list, opcional): Filtros de búsqueda Odoo.
        limit (int, opcional): Máximo de pedidos a devolver.
    """
    return get_pedidos_compra_detallado(domain=domain, limit=limit)

@function_tool
def obtener_lineas_pedido_odoo(order_id: int) -> list:
    """
    Devuelve las líneas de un pedido de compra específico.
    Parámetros:
        order_id (int): ID del pedido de compra.
    """
    return get_lineas_pedido(order_id)
