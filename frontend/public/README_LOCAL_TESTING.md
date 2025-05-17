# Pruebas Locales del Chatbot MagicWave + Odoo

## 1. Backend (API)

Asegúrate de tener todas las dependencias instaladas:

```bash
pip install -r requirements.txt
```

Lanza el backend en modo desarrollo:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

- Cambia la ruta `app.main:app` si tu estructura es diferente.
- El endpoint debe estar disponible en `http://127.0.0.1:8001/chat`.

---

## 2. Frontend (Widget)

Desde la carpeta `frontend/public`, lanza un servidor local:

```bash
python -m http.server 8080
```

Abre en tu navegador:

[http://localhost:8080/index.html](http://localhost:8080/index.html)

---

## 3. Flujo de pruebas

- Escribe un mensaje en el widget y verifica que la petición a `/chat` aparece en la pestaña Network.
- Si hay errores, revisa la consola del navegador y la terminal del backend.
- Si funciona en local pero no en producción, revisa CORS y configuración en Railway.

---

## 4. Cambiar entre local y producción

- Cambia la línea del widget en `index.html` según el entorno.
- Puedes dejar ambas líneas (local y producción) comentadas para facilitar el cambio.

---

## 5. Notas

- Si usas otro puerto, ajusta la URL en el widget.
- Si tienes dudas, revisa el código fuente del widget y asegúrate de que los IDs y endpoints coinciden.

---

¡Listo para depurar y avanzar!
