# Backend - Wingfoil AI CRM

Este backend está construido con FastAPI, integra Odoo y OpenAI Agents, y expone endpoints para el Web Component frontend.

## Estructura

- `app/main.py`: Entrypoint FastAPI, endpoints `/chat` y `/history`.
- `app/odoo_client.py`: Funciones para acceder a la API de Odoo usando variables de entorno.
- `app/ai_agent.py` y `app/ai_agent_tools.py`: Definición y herramientas del agente OpenAI.
- `.env.example`: Plantilla para tus variables de entorno.
- `requirements.txt`: Dependencias del backend.

## Configuración

1. Copia `.env.example` a `.env` y completa tus claves.
2. Instala dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución local

```
uvicorn app.main:app --port 8001
```

## Despliegue en Railway

1. Sube el backend a Railway.
2. Añade las variables de entorno desde `.env.example`.
3. Usa el comando de inicio:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

## Notas
- Las credenciales nunca deben estar hardcodeadas.
- Usa python-dotenv para cargar variables de entorno.
- Consulta la documentación de OpenAI Agents para ampliar el agente.
