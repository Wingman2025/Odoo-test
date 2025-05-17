# Frontend - Web Component Chatbot

Este frontend es un Web Component (`chatbot-widget.js`) que puedes insertar en cualquier web para conectar con el backend de FastAPI.

## Uso rápido

1. Copia `chatbot-widget.js` a tu web o usa el archivo desde `/public`.
2. Añade en tu HTML:
   ```html
   <script src="chatbot-widget.js" type="module"></script>
   <chatbot-widget backend-url="https://TU_BACKEND/chat"></chatbot-widget>
   ```
3. Personaliza estilos o comportamiento editando el JS.

## Desarrollo local

1. Sirve la carpeta `public`:
   ```
   python -m http.server
   ```
2. Abre `http://localhost:8000` en tu navegador.

## Personalización
- Puedes cambiar el color, textos y tamaño editando el archivo JS.
- Puedes usar varios widgets en la misma página cambiando el atributo `backend-url`.
