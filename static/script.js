function sendCommand() {
    const input = document.getElementById('command');
    const core = document.getElementById('jarvis-core');
    const message = input.value.trim();

    if (message === "") return;

    // 1. Add User Message
    appendMessage(message, 'user-msg');
    input.value = "";

    // 2. Start Thinking Animation
    core.classList.remove('idle');
    core.classList.add('thinking');

    // 3. Call Flask API
    fetch("/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: message })
    })
    .then(res => res.json())
    .then(data => {
        appendMessage(data.response, 'bot-msg');
        // Stop thinking animation
        core.classList.remove('thinking');
        core.classList.add('idle');
    })
    .catch(err => {
        appendMessage("Error contacting AI.", 'bot-msg');
        core.classList.remove('thinking');
        core.classList.add('idle');
        console.error(err);
    });
}

function appendMessage(text, className) {
    const chatbox = document.getElementById('chatbox');
    const msgDiv = document.createElement('div');
    msgDiv.className = className;
    msgDiv.innerText = text;
    chatbox.appendChild(msgDiv);

    // Auto-scroll to bottom
    chatbox.scrollTop = chatbox.scrollHeight;
}

// Allow "Enter" key to send message
document.getElementById('command').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendCommand();
    }
});