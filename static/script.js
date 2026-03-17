function sendCommand() {
    const input = document.getElementById('command');
    const core = document.getElementById('jarvis-core');
    const message = input.value.trim();

    if (message === "") return;

    appendMessage(message, 'user-msg');
    input.value = "";

    core.classList.remove('idle');
    core.classList.add('thinking');

    fetch("/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: message })
    })
    .then(res => res.json())
    .then(data => {
        appendMessage(data.response, 'bot-msg');

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
    chatbox.scrollTop = chatbox.scrollHeight;
}

document.getElementById('command').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendCommand();
    }
});