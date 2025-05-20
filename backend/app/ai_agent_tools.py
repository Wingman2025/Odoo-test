"""
ai_agent_tools.py - Herramientas function-calling para el agente AI (wingfoil)
Versión: 0.1.0

Define funciones que acceden a la API de Odoo para obtener información de productos e inventario,
y las registra como herramientas para el agente usando function_tool de openai-agents.
"""

from agents import function_tool
# from app.odoo_client import get_productos, get_inventario # Comentado para reemplazar
from typing import List, Any, Optional
from pydantic import Field
from .odoo_client import (
    get_productos, get_inventario, get_pedidos_compra, get_pedidos_compra_detallado, get_lineas_pedido
)

@function_tool
def obtener_productos_odoo(
    domain: Optional[List[List[Any]]] = Field(default=None, description="Filtro Odoo en formato lista de listas, ej: [['type', '=', 'consu']]. Cada filtro es una lista [campo, operador, valor]."),
    limit: Optional[int] = Field(default=None, description="Máximo de productos a devolver.")
) -> list:
    """
    Devuelve productos de Odoo según filtros y límite opcionales.
    """
    return get_productos(domain=domain, limit=limit)

@function_tool
def obtener_inventario_odoo(
    domain: Optional[List[List[Any]]] = Field(default=None, description="Filtro Odoo en formato lista de listas, ej: [['product_id', '=', 123]]. Cada filtro es una lista [campo, operador, valor]."),
    limit: Optional[int] = Field(default=None, description="Máximo de registros a devolver.")
) -> list:
    """
    Devuelve registros de inventario de Odoo según filtros y límite opcionales.
    """
    return get_inventario(domain=domain, limit=limit)

@function_tool
def obtener_pedidos_compra_odoo(
    domain: Optional[List[List[Any]]] = Field(default=None, description="Filtro Odoo en formato lista de listas, ej: [['state', '=', 'purchase']]. Cada filtro es una lista [campo, operador, valor]."),
    limit: Optional[int] = Field(default=None, description="Máximo de pedidos a devolver.")
) -> list:
    """
    Devuelve pedidos de compra de Odoo según filtros y límite opcionales.
    """
    return get_pedidos_compra(domain=domain, limit=limit)

@function_tool
def obtener_pedidos_compra_detallado_odoo(
    domain: Optional[List[List[Any]]] = Field(default=None, description="Filtro Odoo en formato lista de listas. Cada filtro es una lista [campo, operador, valor]."),
    limit: Optional[int] = Field(default=None, description="Máximo de pedidos a devolver.")
) -> list:
    """
    Devuelve pedidos de compra con líneas anidadas, según filtros y límite opcionales.
    """
    return get_pedidos_compra_detallado(domain=domain, limit=limit)

@function_tool
def obtener_lineas_pedido_odoo(
    order_id: int = Field(..., description="ID del pedido de compra.")
) -> list:
    """
    Devuelve las líneas de un pedido de compra específico.
    """
    return get_lineas_pedido(order_id)
