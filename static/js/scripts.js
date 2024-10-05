// static/js/scripts.js

async function getSentiment() {
    const userText = document.getElementById('userText').value;
    const response = await fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: userText }),
    });
    const data = await response.json();
    document.getElementById('result').innerText = `Sentiment: ${data.sentiment}`;
    addToHistory(userText, data.sentiment);
}

function addToHistory(text, sentiment) {
    const historyList = document.getElementById('historyList');
    const listItem = document.createElement('li');
    listItem.textContent = `${text} - ${sentiment}`;
    historyList.appendChild(listItem);
}
