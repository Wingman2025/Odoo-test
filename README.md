# Proyecto AI Chatbot + Odoo

**Versión:** 0.1.0

Este proyecto implementa una arquitectura profesional y modular para un agente AI conectado a Odoo Online, usando FastAPI como backend y un widget JavaScript personalizado como frontend.

## Estructura

```
my-ai-chatbot-project/
│
├── backend/         # Servicio FastAPI, integración Odoo y OpenAI
│   ├── app/
│   │   ├── main.py
│   │   ├── odoo_client.py
│   │   ├── ai_agent.py
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/        # Widget JS, assets, documentación
│   ├── public/
│   │   ├── index.html
│   │   └── chatbot-widget.js
│   └── README.md
│
└── README.md
```

## Configuración

1. Clona el repositorio.
2. Copia `backend/.env.example` a `backend/.env` y completa tus variables:
    ```
    ODOO_APIKEY=tu_api_key
    ODOO_URL=https://wingsalsa.odoo.com/jsonrpc
    ODOO_DB=wingsalsa
    ODOO_USER=tu_email
    OPENAI_API_KEY=tu_openai_key
    ```
3. Instala dependencias:
    ```
    cd backend
    pip install -r requirements.txt
    ```

## Ejecución local

1. Inicia el backend:
    ```
    uvicorn app.main:app --port 8001
    ```
2. Inicia el frontend:
    ```
    cd ../frontend/public
    python -m http.server
    ```
3. Abre `http://localhost:8000` en tu navegador.

## Despliegue en Railway

1. Sube el código a Railway.
2. Configura las variables de entorno en Railway Dashboard.
3. Railway instalará automáticamente las dependencias de `requirements.txt`.
4. Usa el comando de inicio:
    ```
    uvicorn app.main:app --host 0.0.0.0 --port $PORT
    ```

---

Para más detalles revisa los README en `backend/` y `frontend/`.


## Tecnologías
- Backend: Python 3.10+, FastAPI, openai-agents==0.0.13, openai==1.76
- Frontend: JavaScript (widget embebible)
- Despliegue: Railway

## Descripción breve
- El backend expone una API REST para el widget y conecta con Odoo y OpenAI.
- El frontend es un widget JS fácil de insertar en cualquier web (incluida Odoo Website).
- Separación total entre backend y frontend.

---

## Cómo ejecutar (modo desarrollo)
1. Clonar el repo y entrar en `/backend` y `/frontend`.
2. Instalar dependencias en `/backend`:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el backend:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Abrir `/frontend/public/index.html` en tu navegador para probar el widget.

---

## Despliegue
- El backend está listo para Railway (ver README en `/backend`).
- El frontend se puede servir como estático o incrustar en Odoo Website.

---

## Contacto y soporte
- Documentación detallada en cada subcarpeta.
