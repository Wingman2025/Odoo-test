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
                :host {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 1000;
                    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                }
                .chat-button {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 50%;
                    width: 60px;
                    height: 60px;
                    font-size: 28px;
                    cursor: pointer;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .chatbot-container {
                    width: 360px;
                    height: 500px;
                    background-color: #fff;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    transition: transform 0.3s ease-out, opacity 0.3s ease-out;
                    transform: scale(0.95) translateY(10px);
                    opacity: 0;
                    visibility: hidden;
                }
                .chatbot-container.open {
                    transform: scale(1) translateY(0);
                    opacity: 1;
                    visibility: visible;
                }
                .chatbot-header {
                    background-color: #007bff;
                    color: white;
                    padding: 15px;
                    font-size: 1.1em;
                    font-weight: bold;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .close-button {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.5em;
                    cursor: pointer;
                }
                .chatbot-messages {
                    flex-grow: 1;
                    padding: 15px;
                    overflow-y: auto;
                    background-color: #f7f7f7;
                }
                .message {
                    margin-bottom: 10px;
                    padding: 10px 12px;
                    border-radius: 18px;
                    max-width: 80%;
                    line-height: 1.4;
                }
                .message.user {
                    background-color: #007bff;
                    color: white;
                    align-self: flex-end;
                    margin-left: auto; /* Alinea a la derecha */
                }
                .message.agent {
                    background-color: #e9ecef;
                    color: #333;
                    align-self: flex-start;
                }
                .chatbot-input-area {
                    display: flex;
                    padding: 10px;
                    border-top: 1px solid #ddd;
                    background-color: #fff;
                }
                .chatbot-input {
                    flex-grow: 1;
                    border: 1px solid #ccc;
                    border-radius: 20px;
                    padding: 10px 15px;
                    font-size: 1em;
                    margin-right: 8px;
                    outline: none;
                }
                .chatbot-send-button {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 20px;
                    font-size: 1em;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }
                .chatbot-send-button:hover {
                    background-color: #0056b3;
                }
            </style>
            
            <div class="chatbot-container" id="chatbot-container">
                <div class="chatbot-header">
                    <span>Wingfoil Assistant</span>
                    <button class="close-button" id="close-chat">×</button>
                </div>
                <div class="chatbot-messages" id="messages-area"></div>
                <div class="chatbot-input-area">
                    <input type="text" id="user-input" class="chatbot-input" placeholder="Escribe un mensaje...">
                    <button id="send-button" class="chatbot-send-button">Enviar</button>
                </div>
            </div>
            <button class="chat-button" id="toggle-chat">💬</button>
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
