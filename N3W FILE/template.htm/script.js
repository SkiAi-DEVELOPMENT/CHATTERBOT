document.getElementById('send-button').addEventListener('click', function() {
    sendMessage();
});

document.getElementById('chat-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (message) {
        const chatBox = document.getElementById('chat-box');
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        input.value = '';
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
    }
}
