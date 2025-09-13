// index_script.js

document.addEventListener('DOMContentLoaded', () => {
    const usernameInput = document.getElementById('usernameInput');
    const loginBtn = document.getElementById('loginBtn');
    const startWhereLeftOffCheckbox = document.getElementById('startWhereLeftOff'); // New checkbox reference
    const appNavbarTitle = document.getElementById('app-navbar-title');
    const darkModeToggle = document.getElementById('darkModeToggle');

        // Get the base URL dynamically
    const API_BASE_URL = window.location.origin;

    // --- Dark Mode Logic ---
    function applyTheme(isDarkMode) {
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    }

    // Load theme preference from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        darkModeToggle.checked = true;
        applyTheme(true);
    } else {
        darkModeToggle.checked = false;
        applyTheme(false);
    }

    // Event listener for the dark mode toggle
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

    // Fetch and set app name
    async function fetchAppName() {
        try {
            const response = await fetch(`${API_BASE_URL}/app_name`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            appNavbarTitle.textContent = data.app_name;
            document.title = `Login - ${data.app_name}`; // Update page title as well
        } catch (error) {
            console.error('Error fetching app name:', error);
            appNavbarTitle.textContent = 'ADK Agent (Error)';
            document.title = 'Login - ADK Agent (Error)';
        }
    }

    fetchAppName();

    // Event listener for Login button
    loginBtn.addEventListener('click', () => {
        const username = usernameInput.value.trim();
        if (username) {
            let redirectUrl = `/landing.html?username=${encodeURIComponent(username)}`;

            // If "Start where we left off" is NOT checked, add the query parameter
            if (!startWhereLeftOffCheckbox.checked) {
                redirectUrl += '&start_new_session=Y';
            }

            window.location.href = redirectUrl;
        } else {
            alert('Please enter a username.'); // Simple alert for missing username
        }
    });

    // Allow login with Enter key in username input
    usernameInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default Enter behavior
            loginBtn.click(); // Trigger login button click
        }
    });
});
