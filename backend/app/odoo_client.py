"""
odoo_client.py - Cliente Odoo para FastAPI
Versión: 0.1.0

Este módulo contiene funciones para consultar productos e inventario desde Odoo Online
usando la API JSON-RPC. Configura aquí tus credenciales y lógica de acceso.
"""

import json
import random
import urllib.request

# Configuración Odoo usando variables de entorno y python-dotenv
import os
from dotenv import load_dotenv

load_dotenv()

URL  = os.getenv("ODOO_URL", "https://wingsalsa.odoo.com/jsonrpc")
DB   = os.getenv("ODOO_DB", "wingsalsa")
USER = os.getenv("ODOO_USER", "jorgescm86@gmail.com")
KEY  = os.getenv("ODOO_APIKEY")  # Ahora se obtiene de la variable de entorno

# Utilidad para llamada JSON-RPC

def rpc_call(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(1, 1_000_000)
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        response = urllib.request.urlopen(req).read()
        return json.loads(response)
    except Exception as e:
        return {"error": str(e)}

# Función para obtener productos

def get_productos(domain=None, limit=None):
    """
    Devuelve los productos de Odoo según el dominio y límite especificados.
    Incluye campos clave: nombre, tipo, precio y código.

    Parámetros:
        domain (list, opcional): Filtros de búsqueda Odoo (por defecto, todos los productos).
        limit (int, opcional): Máximo de productos a devolver (por defecto, sin límite).
    """
    # Login
    auth = rpc_call("call", {
        "service": "common",
        "method": "login",
        "args": [DB, USER, KEY]
    })
    uid = auth.get("result")
    if not isinstance(uid, int):
        return {"error": "No se pudo autenticar en Odoo"}
    # Buscar productos
    if domain is None:
        domain = []
    args = [DB, uid, KEY, "product.template", "search", domain]
    if limit is not None:
        args += [0, limit]
    prod_ids = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": args
    })
    pids = prod_ids.get("result", [])
    if not pids or not isinstance(pids, list):
        return {"error": "No se encontraron productos"}
    products = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": [DB, uid, KEY, "product.template", "read", pids, ["name", "type", "list_price", "default_code"]]
    })
    return products.get("result", [])

# Función para obtener pedidos de compra

def get_pedidos_compra(domain=None, limit=None):
    """
    Devuelve los pedidos de compra (purchase.order) de Odoo según el dominio y límite especificados.
    Incluye campos clave: número, proveedor, fecha de pedido y estado.

    Parámetros:
        domain (list, opcional): Filtros de búsqueda Odoo (por defecto, todos los pedidos).
        limit (int, opcional): Máximo de pedidos a devolver (por defecto, sin límite).
    """
    # Login
    auth = rpc_call("call", {
        "service": "common",
        "method": "login",
        "args": [DB, USER, KEY]
    })
    uid = auth.get("result")
    if not isinstance(uid, int):
        return {"error": "No se pudo autenticar en Odoo"}
    # Buscar pedidos de compra
    if domain is None:
        domain = []
    args = [DB, uid, KEY, "purchase.order", "search", domain]
    if limit is not None:
        args += [0, limit]
    po_ids = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": args
    })
    ids = po_ids.get("result", [])
    if not ids or not isinstance(ids, list):
        return {"error": "No se encontraron pedidos de compra"}
    # Leer campos relevantes
    pedidos = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": [DB, uid, KEY, "purchase.order", "read", ids, ["name", "partner_id", "date_order", "state"]]
    })
    return pedidos.get("result", [])

# Función para obtener líneas de un pedido de compra

def get_lineas_pedido(order_id, uid=None):
    """
    Devuelve las líneas de un pedido de compra, incluyendo producto, cantidad y almacén destino.
    """
    # Login solo si no se proporciona uid
    if uid is None:
        auth = rpc_call("call", {
            "service": "common",
            "method": "login",
            "args": [DB, USER, KEY]
        })
        uid = auth.get("result")
        if not isinstance(uid, int):
            return {"error": "No se pudo autenticar en Odoo"}
    # Buscar líneas del pedido
    lineas = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": [DB, uid, KEY, "purchase.order.line", "search_read", [["order_id", "=", order_id]], ["product_id", "product_qty", "product_uom", "date_planned", "location_dest_id"]]
    })
    return lineas.get("result", [])

# Función extendida para obtener pedidos de compra con líneas anidadas

def get_pedidos_compra_detallado(domain=None, limit=None):
    """
    Devuelve los pedidos de compra de Odoo, cada uno con sus líneas (productos, cantidades, almacén destino).

    Parámetros:
        domain (list, opcional): Filtros de búsqueda Odoo (por defecto, todos los pedidos).
        limit (int, opcional): Máximo de pedidos a devolver (por defecto, sin límite).
    """
    # Login
    auth = rpc_call("call", {
        "service": "common",
        "method": "login",
        "args": [DB, USER, KEY]
    })
    uid = auth.get("result")
    if not isinstance(uid, int):
        return {"error": "No se pudo autenticar en Odoo"}
    # Buscar pedidos de compra
    if domain is None:
        domain = []
    args = [DB, uid, KEY, "purchase.order", "search", domain]
    if limit is not None:
        args += [0, limit]
    po_ids = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": args
    })
    ids = po_ids.get("result", [])
    if not ids or not isinstance(ids, list):
        return {"error": "No se encontraron pedidos de compra"}
    # Leer campos relevantes
    pedidos = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": [DB, uid, KEY, "purchase.order", "read", ids, ["name", "partner_id", "date_order", "state"]]
    })
    pedidos_list = pedidos.get("result", [])
    # Para cada pedido, obtener sus líneas
    for pedido in pedidos_list:
        pedido_id = pedido["id"]
        pedido["lineas"] = get_lineas_pedido(pedido_id, uid=uid)
    return pedidos_list

# Función para obtener inventario

def get_inventario(domain=None, limit=None):
    """
    Devuelve los registros de inventario de Odoo según el dominio y límite especificados.
    Incluye campos clave: producto, cantidad y ubicación.

    Parámetros:
        domain (list, opcional): Filtros de búsqueda Odoo (por defecto, todo el inventario).
        limit (int, opcional): Máximo de registros a devolver (por defecto, sin límite).
    """
    # Login
    auth = rpc_call("call", {
        "service": "common",
        "method": "login",
        "args": [DB, USER, KEY]
    })
    uid = auth.get("result")
    if not isinstance(uid, int):
        return {"error": "No se pudo autenticar en Odoo"}
    # Buscar inventarios
    if domain is None:
        domain = []
    args = [DB, uid, KEY, "stock.quant", "search", domain]
    if limit is not None:
        args += [0, limit]
    inv_ids = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": args
    })
    iids = inv_ids.get("result", [])
    if not iids or not isinstance(iids, list):
        return {"error": "No se encontraron registros de inventario"}
    inventarios = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": [DB, uid, KEY, "stock.quant", "read", iids, ["product_id", "quantity", "location_id"]]
    })
    return inventarios.get("result", [])
