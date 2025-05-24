"""
visualiza_grafos.py - Script para generar diagramas de orquestación de agentes (Graphviz)
Versión: 1.0.0

Este script importa los agentes principales definidos en ai_agent.py y genera archivos PNG
de visualización de su estructura y handoffs usando draw_graph del SDK openai-agents.

Ejecución:
    cd backend/app
    python visualiza_grafos.py

Los archivos PNG se generarán en el mismo directorio.
"""

import sys
import os
sys.path.insert(0, os.path.abspath("."))  # Añade backend/app al sys.path
sys.path.insert(0, os.path.abspath("..")) # Añade backend/ al sys.path

from ai_agent import triage_agent, crm_agent, internal_ops_agent
from agents.extensions.visualization import draw_graph

# Generar diagramas para cada agente principal
print("Generando diagramas de agentes...")
draw_graph(triage_agent, filename="triage_agent_graph")
draw_graph(crm_agent, filename="crm_agent_graph")
draw_graph(internal_ops_agent, filename="internal_ops_agent_graph")
print("Diagramas generados: triage_agent_graph.png, crm_agent_graph.png, internal_ops_agent_graph.png")
