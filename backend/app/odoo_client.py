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

def get_productos():
    """Devuelve los primeros 10 productos de Odoo"""
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
    prod_ids = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": [DB, uid, KEY, "product.template", "search", [], 0, 10]
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

# Función para obtener inventario

def get_inventario():
    """Devuelve los primeros 10 registros de inventario de Odoo"""
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
    inv_ids = rpc_call("call", {
        "service": "object",
        "method": "execute",
        "args": [DB, uid, KEY, "stock.quant", "search", [], 0, 10]
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
