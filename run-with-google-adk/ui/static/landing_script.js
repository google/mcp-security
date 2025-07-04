// landing_script.js

document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const submitBtn = document.getElementById('submit-btn');
    const logoutBtn = document.getElementById('logoutBtn');
    const sessionInfoDiv = document.getElementById('session-info');
    const appNavbarTitle = document.getElementById('app-navbar-title');
    const darkModeToggle = document.getElementById('darkModeToggle');

    // Get the base URL dynamically
    const API_BASE_URL = window.location.origin;    

    let currentSessionId = null;
    let currentUserId = null;
    let requestSentTime = 0;
    let lastAgentMessageTime = 0; // Re-introduced for per-chunk timing
    let waitingMessageElement = null; // Reference to the "waiting" message element
    // currentAgentResponseBuffer is no longer needed as we are streaming, not buffering.

    // Get username from URL query parameter
    const urlParams = new URLSearchParams(window.location.search);
    const username = urlParams.get('username');
    const startNewSessionParam = urlParams.get('start_new_session'); // This line reads the new parameter


    if (!username) {
        alert('Username not provided. Redirecting to login page.');
        window.location.href = '/';
        return;
    }

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
    // timeDiff parameter is re-introduced for agent messages
    function appendMessage(text, sender, timeElapsed = null, timeDiff = null, isWaiting = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        if (isWaiting) {
            messageDiv.classList.add('waiting'); // Add 'waiting' class for special styling
        }

        // Only show time for actual messages, not the waiting message
        if (timeElapsed !== null && !isWaiting) {
            const timeDisplay = document.createElement('div');
            timeDisplay.classList.add('message-time');
            let timeText = `${timeElapsed}ms`;
            if (timeDiff !== null && sender === 'agent') { // Show diff for agent messages
                timeText += ` (${timeDiff}ms)`;
            }
            timeDisplay.textContent = timeText;
            messageDiv.appendChild(timeDisplay);
        }

        const messageContent = document.createElement('div'); // Container for the actual message text/markdown
        if (sender === 'agent' && !isWaiting) { // Render markdown for actual agent messages
            messageContent.innerHTML = marked.parse(text);
        } else {
            messageContent.textContent = text;
        }
        messageDiv.appendChild(messageContent); // Append content after time (if time is present)

        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return messageDiv; // Return the created message element
    }

    // Fetch and set app name
    async function fetchAppName() {
        try {
            const response = await fetch(`${API_BASE_URL}/app_name`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            appNavbarTitle.textContent = data.app_name;
            document.title = `Chat - ${data.app_name}`;
        } catch (error) {
            console.error('Error fetching app name:', error);
            appNavbarTitle.textContent = 'ADK Agent (Error)';
            document.title = 'Chat - ADK Agent (Error)';
        }
    }

    // Function to fetch the session ID and user ID
    async function fetchSessionAndUserId() {
        let apiUrl = `${API_BASE_URL}/get_session?username=${encodeURIComponent(username)}`;

        // If start_new_session=Y is present in the URL, add it to the API call
        if (startNewSessionParam === 'Y') { // This conditional logic adds it to the API URL
            apiUrl += '&start_new_session=Y';
        }else{
            apiUrl += '&start_new_session=N';
        }

        try {
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            currentSessionId = data.session_id;
            currentUserId = data.user_id;
            sessionInfoDiv.textContent = `Session ID: ${currentSessionId} | User: ${currentUserId}`;
            sessionInfoDiv.classList.remove('alert-info');
            sessionInfoDiv.classList.add('alert-success');
            console.log('Session ID fetched:', currentSessionId, 'User ID:', currentUserId);
            submitBtn.disabled = false;
            userInput.disabled = false;
        } catch (error) {
            console.error('Error fetching session/user ID:', error);
            sessionInfoDiv.textContent = 'Error loading session/user ID.';
            sessionInfoDiv.classList.remove('alert-info');
            sessionInfoDiv.classList.add('alert-danger');
            submitBtn.disabled = true;
            userInput.disabled = true;
        }
    }

    // Initial calls on page load
    fetchAppName();
    fetchSessionAndUserId();
    submitBtn.disabled = true;
    userInput.disabled = true;


    // Event listener for the Submit button
    submitBtn.addEventListener('click', async () => {
        const message = userInput.value.trim();
        if (!currentSessionId || !currentUserId) {
            appendMessage('Error: Session or User ID not available. Please refresh the page.', 'agent');
            return;
        }
        if (message) {
            appendMessage(message, 'user', 0); // Display user message immediately
            userInput.value = ''; // Clear input field

            // Append the waiting message
            // Note: timeElapsed is null as the waiting message itself doesn't have an elapsed time.
            waitingMessageElement = appendMessage('Agent is responding ...', 'agent', null, null, true);

            requestSentTime = Date.now(); // Record time of request initiation
            lastAgentMessageTime = requestSentTime; // Initialize for first agent chunk


            try {
                const response = await fetch(`${API_BASE_URL}/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        session_id: currentSessionId,
                        user_id: currentUserId,
                        message: message
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const reader = response.body.getReader();
                const decoder = new TextDecoder('utf-8');
                let buffer = '';

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) {
                        console.log('Stream finished (no last_msg received, or natural end).');
                        // If stream ends without explicit last_msg=true, just remove waiting message
                        break;
                    }
                    buffer += decoder.decode(value, { stream: true });

                    let boundary = buffer.indexOf('\n\n');
                    while (boundary !== -1) {
                        const chunk = buffer.substring(0, boundary);
                        buffer = buffer.substring(boundary + 2); // +2 for '\n\n'

                        if (chunk.startsWith('data: ')) {
                            try {
                                const jsonString = chunk.substring(6); // Remove 'data: '
                                const data = JSON.parse(jsonString);

                                if (data.last_msg && data.text === 'Stream finished.') {
                                    console.log('SSE connection closed by last_msg signal.');
                                    reader.cancel(); // Stop reading from the stream
                                    break; // Exit the inner while loop to clean up waiting message
                                } else {
                                    // Calculate timing for each received chunk
                                    const receivedTime = Date.now();
                                    const timeElapsed = receivedTime - requestSentTime;
                                    const timeDiff = receivedTime - lastAgentMessageTime;
                                    lastAgentMessageTime = receivedTime; // Update for next chunk

                                    // Append each agent message chunk as it arrives
                                    appendMessage(data.text, 'agent', timeElapsed, timeDiff);
                                }
                            } catch (parseError) {
                                console.error('Error parsing JSON chunk:', parseError, 'Chunk:', chunk);
                                // If parsing fails, just log and continue, or append error message if needed
                            }
                        }
                        boundary = buffer.indexOf('\n\n');
                    }
                    if (done) break; // Break outer loop if stream is done and all chunks processed
                }

            } catch (error) {
                console.error('Failed to connect to chat or stream error:', error);
                // If an error occurs, update the waiting message or append a new error message
                if (waitingMessageElement) {
                    waitingMessageElement.textContent = 'Error: Failed to get response. Stream interrupted.';
                    waitingMessageElement.classList.remove('waiting');
                    waitingMessageElement.classList.add('text-danger'); // Bootstrap class for red text
                } else {
                    appendMessage('Error initiating chat or stream failed unexpectedly.', 'agent');
                }
            } finally {
                // Ensure waiting message is removed/updated when the entire stream finishes or errors
                if (waitingMessageElement) {
                    chatWindow.removeChild(waitingMessageElement);
                    waitingMessageElement = null;
                }
            }
        }
    });

    // Removed Clear button event listener
    // clearBtn.addEventListener('click', () => {
    //     chatWindow.innerHTML = '';
    // });

    // Event listener for Logout button
    logoutBtn.addEventListener('click', () => {
        currentSessionId = null;
        currentUserId = null;
        window.location.href = '/';
    });

    // Allow sending message with Enter key
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            submitBtn.click();
        }
    });
});
