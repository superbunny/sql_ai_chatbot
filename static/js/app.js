// DOM Elements
const welcomeScreen = document.getElementById('welcomeScreen');
const chatScreen = document.getElementById('chatScreen');
const dbUpload = document.getElementById('dbUpload');
const uploadBtn = document.getElementById('uploadBtn');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeModal = document.getElementById('closeModal');
const schemaViewer = document.getElementById('schemaViewer');
const dataDictionary = document.getElementById('dataDictionary');
const updateDictionaryBtn = document.getElementById('updateDictionaryBtn');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const newChatBtn = document.getElementById('newChatBtn');
const loadingOverlay = document.getElementById('loadingOverlay');

// State
let isProcessing = false;

// Event Listeners
uploadBtn.addEventListener('click', () => {
    dbUpload.click();
});

dbUpload.addEventListener('change', handleDatabaseUpload);

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

settingsBtn.addEventListener('click', () => {
    settingsModal.classList.add('show');
    loadSchema();
});

closeModal.addEventListener('click', () => {
    settingsModal.classList.remove('show');
});

settingsModal.addEventListener('click', (e) => {
    if (e.target === settingsModal) {
        settingsModal.classList.remove('show');
    }
});

updateDictionaryBtn.addEventListener('click', updateDataDictionary);

clearHistoryBtn.addEventListener('click', clearHistory);

newChatBtn.addEventListener('click', startNewChat);

// Suggestion cards
document.querySelectorAll('.suggestion-card').forEach(card => {
    card.addEventListener('click', () => {
        const question = card.querySelector('h4').textContent;
        if (chatScreen.style.display !== 'none') {
            chatInput.value = question;
            chatInput.focus();
        }
    });
});

// Functions
async function handleDatabaseUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('database', file);

    showLoading();

    try {
        const response = await fetch('/upload_db', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            showError(data.error);
        } else {
            showChatScreen();
            showSuccess('Database uploaded successfully!');
        }
    } catch (error) {
        showError('Failed to upload database: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function sendMessage() {
    if (isProcessing || !chatInput.value.trim()) return;

    const message = chatInput.value.trim();
    chatInput.value = '';
    isProcessing = true;
    sendBtn.disabled = true;

    // Add user message
    addMessage(message, 'user');

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator(typingId);

        if (data.error) {
            addMessage('Error: ' + data.error, 'assistant');
        } else {
            addMessage(data.message, 'assistant', {
                sqlQuery: data.sql_query,
                results: data.results,
                visualization: data.visualization,
                error: data.error
            });
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('Failed to send message: ' + error.message, 'assistant');
    } finally {
        isProcessing = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

function addMessage(text, role, extras = {}) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';

    const content = document.createElement('div');
    content.className = 'message-content';

    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = text;
    content.appendChild(messageText);

    // Add SQL query if present
    if (extras.sqlQuery) {
        const sqlDiv = document.createElement('div');
        sqlDiv.className = 'sql-query';
        const pre = document.createElement('pre');
        pre.textContent = extras.sqlQuery;
        sqlDiv.appendChild(pre);
        content.appendChild(sqlDiv);
    }

    // Add error if present
    if (extras.error) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = 'SQL Error: ' + extras.error;
        content.appendChild(errorDiv);
    }

    // Add results table if present
    if (extras.results && extras.results.data.length > 0) {
        const resultsDiv = document.createElement('div');
        resultsDiv.className = 'query-results';

        const resultHeader = document.createElement('div');
        resultHeader.className = 'result-header';
        resultHeader.innerHTML = `✅ Returned ${extras.results.row_count} rows`;
        resultsDiv.appendChild(resultHeader);

        const table = document.createElement('table');
        table.className = 'results-table';

        // Table header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        extras.results.columns.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Table body
        const tbody = document.createElement('tbody');
        extras.results.data.forEach(row => {
            const tr = document.createElement('tr');
            extras.results.columns.forEach(col => {
                const td = document.createElement('td');
                td.textContent = row[col] !== null ? row[col] : 'NULL';
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);

        resultsDiv.appendChild(table);
        content.appendChild(resultsDiv);
    }

    // Add visualization if present
    if (extras.visualization) {
        const vizDiv = document.createElement('div');
        vizDiv.className = 'visualization';
        const img = document.createElement('img');
        img.src = 'data:image/png;base64,' + extras.visualization;
        img.alt = 'Data Visualization';
        vizDiv.appendChild(img);
        content.appendChild(vizDiv);
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
    const id = 'typing-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = id;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';

    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = '<div class="message-text">Thinking...</div>';

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return id;
}

function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

function showChatScreen() {
    welcomeScreen.style.display = 'none';
    chatScreen.style.display = 'flex';
    chatInput.focus();
}

async function loadSchema() {
    try {
        const response = await fetch('/get_schema');
        const data = await response.json();
        
        if (data.schema) {
            schemaViewer.textContent = data.schema;
        } else {
            schemaViewer.innerHTML = '<p class="text-muted">Upload a database to view schema</p>';
        }
    } catch (error) {
        schemaViewer.innerHTML = '<p class="text-muted">Failed to load schema</p>';
    }
}

async function updateDataDictionary() {
    try {
        const dictionary = dataDictionary.value.trim();
        
        const response = await fetch('/update_dictionary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ dictionary })
        });

        const data = await response.json();

        if (data.error) {
            showError(data.error);
        } else {
            showSuccess('Data dictionary updated!');
        }
    } catch (error) {
        showError('Failed to update dictionary: ' + error.message);
    }
}

async function clearHistory() {
    if (!confirm('Are you sure you want to clear the chat history?')) return;

    try {
        const response = await fetch('/clear_history', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            chatMessages.innerHTML = '';
            showSuccess('Chat history cleared!');
        }
    } catch (error) {
        showError('Failed to clear history: ' + error.message);
    }
}

async function startNewChat() {
    if (!confirm('Start a new chat? Current history will be cleared.')) return;

    try {
        const response = await fetch('/new_chat', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            chatMessages.innerHTML = '';
            welcomeScreen.style.display = 'flex';
            chatScreen.style.display = 'none';
            showSuccess('New chat started!');
        }
    } catch (error) {
        showError('Failed to start new chat: ' + error.message);
    }
}

function showLoading() {
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

function showError(message) {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = 'toast error';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: var(--error-red);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        z-index: 3000;
        animation: slideIn 0.3s ease-out;
    `;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function showSuccess(message) {
    const toast = document.createElement('div');
    toast.className = 'toast success';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: var(--success-green);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        z-index: 3000;
        animation: slideIn 0.3s ease-out;
    `;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
