/**
 * chatbot-widget.js - Web Component para el chat de IA con Odoo
 * Versión: 0.1.0
 *
 * Este archivo define un Web Component reutilizable para integrar el chatbot en cualquier web.
 * El componente se comunica con el backend FastAPI a través del endpoint /chat.
 *
 * Uso:
 * <chatbot-widget backend-url="http://localhost:8001/chat"></chatbot-widget>
 *
 * Puedes personalizar el estilo y comportamiento extendiendo este archivo.
 */

class ChatbotWidget extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.backendUrl = this.getAttribute('backend-url') || 'http://localhost:8001/chat'; // URL por defecto
        this.chatHistory = []; // Para mantener el historial de la conversación
        this.isChatOpen = false; // Estado para controlar si el chat está abierto o minimizado

        this.shadowRoot.innerHTML = `
            <style>
                /* Fuente y colores MagicWave */
                @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
                :host {
                    position: fixed;
                    bottom: 24px;
                    right: 24px;
                    z-index: 1000;
                    font-family: 'Montserrat', system-ui, sans-serif;
                }
                /* Burbuja del chat (MagicWave look) */
                .chat-button {
                    background: linear-gradient(135deg, #00aaff 60%, #0099dd 100%);
                    color: #fff;
                    border: none;
                    border-radius: 50%;
                    width: 62px;
                    height: 62px;
                    font-size: 32px;
                    cursor: pointer;
                    box-shadow: 0 6px 16px rgba(0,170,255,0.25);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: box-shadow 0.2s, background 0.2s;
                }
                .chat-button:hover {
                    box-shadow: 0 8px 24px rgba(0,170,255,0.35);
                    background: linear-gradient(135deg, #0099dd 60%, #00aaff 100%);
                }
                /* Contenedor principal del chat */
                .chatbot-container {
                    width: 370px;
                    height: 520px;
                    background: #fff;
                    border-radius: 18px;
                    box-shadow: 0 8px 32px rgba(0,170,255,0.12);
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    transition: transform 0.3s, opacity 0.3s;
                    transform: scale(0.97) translateY(10px);
                    opacity: 0;
                    visibility: hidden;
                }
                .chatbot-container.open {
                    transform: scale(1) translateY(0);
                    opacity: 1;
                    visibility: visible;
                }
                /* Cabecera MagicWave */
                .chatbot-header {
                    background: linear-gradient(90deg, #00aaff 70%, #0099dd 100%);
                    color: white;
                    padding: 16px 18px;
                    font-size: 1.1em;
                    font-weight: bold;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-top-left-radius: 18px;
                    border-top-right-radius: 18px;
                    box-shadow: 0 2px 8px rgba(0,170,255,0.10);
                }
                .header-logo {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                .header-logo svg {
                    height: 28px;
                    width: 90px;
                }
                .close-button {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.7em;
                    cursor: pointer;
                    opacity: 0.8;
                    transition: opacity 0.2s;
                }
                .close-button:hover {
                    opacity: 1;
                }
                /* Mensajes */
                .chatbot-messages {
                    flex-grow: 1;
                    padding: 18px 14px;
                    overflow-y: auto;
                    background: #f6fafd;
                }
                .message {
                    margin-bottom: 12px;
                    padding: 12px 16px;
                    border-radius: 20px;
                    max-width: 80%;
                    line-height: 1.5;
                    font-size: 1em;
                    word-break: break-word;
                }
                .message.user {
                    background: linear-gradient(135deg, #00aaff 70%, #0099dd 100%);
                    color: white;
                    align-self: flex-end;
                    margin-left: auto;
                    border-bottom-right-radius: 8px;
                }
                .message.agent {
                    background: #e9f7fd;
                    color: #222;
                    align-self: flex-start;
                    border-bottom-left-radius: 8px;
                }
                /* Área de entrada */
                .chatbot-input-area {
                    display: flex;
                    padding: 12px 14px;
                    border-top: 1px solid #e0e9ef;
                    background: #fff;
                }
                .chatbot-input {
                    flex-grow: 1;
                    border: 1.5px solid #00aaff;
                    border-radius: 22px;
                    padding: 12px 16px;
                    font-size: 1em;
                    margin-right: 10px;
                    outline: none;
                    background: #fafdff;
                    transition: border 0.2s;
                }
                .chatbot-input:focus {
                    border-color: #0099dd;
                }
                .chatbot-send-button {
                    background: linear-gradient(135deg, #00aaff 70%, #0099dd 100%);
                    color: white;
                    border: none;
                    border-radius: 22px;
                    padding: 10px 22px;
                    font-size: 1em;
                    cursor: pointer;
                    font-weight: 600;
                    transition: background 0.2s;
                }
                .chatbot-send-button:hover {
                    background: linear-gradient(135deg, #0099dd 70%, #00aaff 100%);
                }
            </style>
            
            <div class="chatbot-container" id="chatbot-container">
                <div class="chatbot-header">
                    <!-- Logo MagicWave en la cabecera del chat -->
                    <span class="header-logo" style="display:flex;align-items:center;gap:10px;">
                        <img src="logosolo.png" alt="Logo" style="height:28px;width:auto;max-width:110px;object-fit:contain;vertical-align:middle;" />
                        <span style="font-weight:700;font-size:1.08em;letter-spacing:0.5px;">Assistant</span>
                    </span>
                    <!-- Se agrega id 'close-chat' para que el selector JS funcione correctamente -->
<button class="close-button" id="close-chat" title="Cerrar">&times;</button>
                </div>
                <div class="chatbot-messages" id="messages-area"></div>
                <div class="chatbot-input-area">
                    <input type="text" id="user-input" class="chatbot-input" placeholder="Escribe un mensaje...">
                    <button id="send-button" class="chatbot-send-button">Enviar</button>
                </div>
            </div>
            <button class="chat-button" id="toggle-chat" style="background: transparent; box-shadow: none; overflow: hidden; padding: 0;">
                <img src="logosolo.png" alt="Chat" style="width: 100%; height: 100%; object-fit: contain; padding: 10px;">
            </button>
        `;
    }

    connectedCallback() {
        this.ui = {
            toggleChatButton: this.shadowRoot.getElementById('toggle-chat'),
            closeChatButton: this.shadowRoot.getElementById('close-chat'),
            chatContainer: this.shadowRoot.getElementById('chatbot-container'),
            sendButton: this.shadowRoot.getElementById('send-button'),
            userInput: this.shadowRoot.getElementById('user-input'),
            messagesArea: this.shadowRoot.getElementById('messages-area'),
        };

        this.ui.toggleChatButton.addEventListener('click', () => this.toggleChat());
        this.ui.closeChatButton.addEventListener('click', () => this.closeChat());
        this.ui.sendButton.addEventListener('click', () => this.handleSendMessage());
        this.ui.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleSendMessage();
            }
        });
        // Mensaje de bienvenida inicial del agente
        this.addMessageToUI("¡Hola! Soy tu asistente virtual de Wingfoil. ¿En qué puedo ayudarte hoy?", 'agent');
    }

    toggleChat() {
        this.isChatOpen = !this.isChatOpen;
        if (this.isChatOpen) {
            this.ui.chatContainer.classList.add('open');
            this.ui.toggleChatButton.style.display = 'none'; // Ocultar botón de burbuja
        } else {
            this.ui.chatContainer.classList.remove('open');
            this.ui.toggleChatButton.style.display = 'flex'; // Mostrar botón de burbuja
        }
    }

    openChat() {
        if (!this.isChatOpen) {
            this.toggleChat();
        }
    }

    closeChat() {
        if (this.isChatOpen) {
            this.toggleChat();
        }
    }

    async handleSendMessage() {
        const messageText = this.ui.userInput.value.trim();
        if (!messageText) return;

        this.addMessageToUI(messageText, 'user');
        this.chatHistory.push({ role: 'user', content: messageText });
        this.ui.userInput.value = '';
        this.scrollToBottom();

        // Prepara el cuerpo de la solicitud para el backend
        const requestBody = {
            history: this.chatHistory.slice(0, -1), // Envía todo el historial excepto el último mensaje del usuario
            user_message: messageText
        };

        try {
            const response = await fetch(this.backendUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Error desconocido del servidor' }));
                throw new Error(`Error del servidor: ${response.status} ${errorData.detail || response.statusText}`);
            }

            const data = await response.json();
            if (data.response) {
                this.addMessageToUI(data.response, 'agent');
                this.chatHistory.push({ role: 'assistant', content: data.response });
            } else {
                this.addMessageToUI('No se recibió respuesta del agente.', 'agent');
            }
        } catch (error) {
            console.error('Error al enviar mensaje:', error);
            this.addMessageToUI(`Error: ${error.message || 'No se pudo conectar con el servidor.'}`, 'agent');
        }
        this.scrollToBottom();
    }

    addMessageToUI(text, role) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', role);
        messageElement.textContent = text;
        this.ui.messagesArea.appendChild(messageElement);
        this.scrollToBottom();
    }

    scrollToBottom() {
        this.ui.messagesArea.scrollTop = this.ui.messagesArea.scrollHeight;
    }
}

// Definir el elemento personalizado
if (!customElements.get('chatbot-widget')) {
    customElements.define('chatbot-widget', ChatbotWidget);
}
