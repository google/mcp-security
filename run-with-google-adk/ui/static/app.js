// app.js

document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const submitBtn = document.getElementById('submit-btn');
    const clearBtn = document.getElementById('clear-btn');
    const sessionInfoDiv = document.getElementById('session-info');
    const darkModeToggle = document.getElementById('darkModeToggle');

    let currentSessionId = null; // Variable to store the session ID
    let requestSentTime = 0; // Timestamp when the user message was sent
    let lastAgentMessageTime = 0; // Timestamp of the last received agent message

    // --- Dark Mode Logic ---
    function applyTheme(isDarkMode) {
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    }

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        darkModeToggle.checked = true;
        applyTheme(true);
    } else {
        darkModeToggle.checked = false;
        applyTheme(false);
    }

    darkModeToggle.addEventListener('change', () => {
        if (darkModeToggle.checked) {
            applyTheme(true);
            localStorage.setItem('theme', 'dark');
        } else {
            applyTheme(false);
            localStorage.setItem('theme', 'light');
        }
    });
    // --- End Dark Mode Logic ---


    // Function to append a message to the chat window
    // Now accepts timeElapsed and timeDiff parameters
    function appendMessage(text, sender, timeElapsed = null, timeDiff = null) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        // Create and append the time display element if timeElapsed is provided
        if (timeElapsed !== null) {
            const timeDisplay = document.createElement('div');
            timeDisplay.classList.add('message-time');
            let timeText = `${timeElapsed}ms`;
            if (timeDiff !== null && sender === 'agent') { // Only show diff for agent messages
                timeText += ` (${timeDiff}ms)`;
            }
            timeDisplay.textContent = timeText;
            messageDiv.appendChild(timeDisplay);
        }

        const messageContent = document.createElement('div'); // Container for the actual message text/markdown
        if (sender === 'agent') {
            messageContent.innerHTML = marked.parse(text);
        } else {
            messageContent.textContent = text;
        }
        messageDiv.appendChild(messageContent); // Append content after time
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Function to fetch the session ID
    async function fetchSessionId() {
        try {
            const response = await fetch('http://localhost:8000/get_session');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            currentSessionId = data.session_id;
            sessionInfoDiv.textContent = `Session ID: ${currentSessionId}`;
            sessionInfoDiv.classList.remove('alert-info');
            sessionInfoDiv.classList.add('alert-success');
            console.log('Session ID fetched:', currentSessionId);
            submitBtn.disabled = false; // Enable submit button once session is loaded
            userInput.disabled = false; // Enable input once session is loaded
        } catch (error) {
            console.error('Error fetching session ID:', error);
            sessionInfoDiv.textContent = 'Error loading session ID.';
            sessionInfoDiv.classList.remove('alert-info');
            sessionInfoDiv.classList.add('alert-danger');
            // Disable submit button if session ID cannot be fetched
            submitBtn.disabled = true;
            userInput.disabled = true;
        }
    }

    // Fetch session ID on page load
    fetchSessionId();
    // Initially disable submit button until session ID is loaded
    submitBtn.disabled = true;
    userInput.disabled = true;


    // Event listener for the Submit button
    submitBtn.addEventListener('click', async () => {
        const message = userInput.value.trim();
        if (!currentSessionId) {
            appendMessage('Error: Session ID not available. Please refresh the page.', 'agent');
            return;
        }
        if (message) {
            // Display user message immediately with 0ms elapsed time
            appendMessage(message, 'user', 0);
            userInput.value = ''; // Clear input field

            // Capture the time just before sending the request
            requestSentTime = Date.now();
            lastAgentMessageTime = requestSentTime; // Reset for new request

            // Make a request to the /chat API using Server-Sent Events (SSE)
            try {
                const eventSource = new EventSource(`http://localhost:8000/chat?message=${encodeURIComponent(message)}&session_id=${encodeURIComponent(currentSessionId)}`);

                eventSource.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    const receivedTime = Date.now();
                    const timeElapsed = receivedTime - requestSentTime;
                    const timeDiff = receivedTime - lastAgentMessageTime; // Calculate difference from previous agent message
                    lastAgentMessageTime = receivedTime; // Update last agent message time

                    // Do not show "Stream finished." message
                    if (data.last_msg && data.text === 'Stream finished.') {
                        eventSource.close(); // Close the connection when last_msg is true
                        console.log('SSE connection closed.');
                        return; // Do not append this message
                    }

                    // Display agent message with calculated elapsed time and difference
                    appendMessage(data.text, 'agent', timeElapsed, timeDiff);

                    if (data.last_msg) {
                        eventSource.close(); // Close the connection when last_msg is true
                        console.log('SSE connection closed.');
                    }
                };

                eventSource.onerror = (error) => {
                    console.error('EventSource failed:', error);
                    eventSource.close();
                    appendMessage('Error receiving response from agent or stream ended unexpectedly.', 'agent');
                };

            } catch (error) {
                console.error('Failed to connect to SSE:', error);
                appendMessage('Failed to initiate chat session.', 'agent');
            }
        }
    });

    // Event listener for the Clear button
    clearBtn.addEventListener('click', () => {
        chatWindow.innerHTML = ''; // Clear all messages from the chat window
        // Optionally, re-fetch session ID or clear it if desired
    });

    // Allow sending message with Enter key
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) { // Shift+Enter for new line
            event.preventDefault(); // Prevent default Enter behavior (new line)
            submitBtn.click(); // Trigger submit button click
        }
    });
});
