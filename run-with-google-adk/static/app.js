// Google SecOps AI Assistant - Modernized Zero-Build Web Client
// Single-Page Architecture with SSE Streaming, Toast Notifications, and Dynamic MCP Status

document.addEventListener('DOMContentLoaded', () => {
  const API_BASE_URL = window.location.origin;

  // DOM Elements
  const messagesContainer = document.getElementById('messagesContainer');
  const chatTextarea = document.getElementById('chatTextarea');
  const sendBtn = document.getElementById('sendBtn');
  const cancelBtn = document.getElementById('cancelBtn');
  const newInvestigationBtn = document.getElementById('newInvestigationBtn');
  const appTitle = document.getElementById('appTitle');
  const currentSessionDisplay = document.getElementById('currentSessionDisplay');
  const currentUserDisplay = document.getElementById('currentUserDisplay');
  const userAvatar = document.getElementById('userAvatar');
  const userChip = document.getElementById('userChip');
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const toastContainer = document.getElementById('toastContainer');
  const emptyState = document.getElementById('emptyState');
  
  // Modal Elements
  const userModal = document.getElementById('userModal');
  const usernameInput = document.getElementById('usernameInput');
  const saveUserBtn = document.getElementById('saveUserBtn');
  const cancelUserBtn = document.getElementById('cancelUserBtn');

  // MCP Pills
  const pillSecops = document.getElementById('pillSecops');
  const pillScc = document.getElementById('pillScc');
  const pillGti = document.getElementById('pillGti');
  const pillSoar = document.getElementById('pillSoar');

  // Application State
  let currentSessionId = null;
  const savedUser = localStorage.getItem('username');
  let currentUserId = (savedUser && savedUser !== 'secops_user') ? savedUser : null;
  let isStreaming = false;
  let activeAbortController = null;
  let requestStartTime = 0;
  let lastChunkTime = 0;

  // Initialize Theme
  function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      document.documentElement.setAttribute('data-theme', savedTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
      document.documentElement.setAttribute('data-theme', 'light');
    } else {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  }

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    showToast(`Theme switched to ${newTheme} mode`, 'info', 2000);
  }

  // Toast Notification System
  function showToast(message, type = 'info', duration = 3500) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const textSpan = document.createElement('span');
    textSpan.textContent = message;
    toast.appendChild(textSpan);

    const closeBtn = document.createElement('button');
    closeBtn.className = 'toast-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.onclick = () => removeToast(toast);
    toast.appendChild(closeBtn);

    toastContainer.appendChild(toast);

    const timer = setTimeout(() => {
      removeToast(toast);
    }, duration);

    function removeToast(el) {
      clearTimeout(timer);
      el.style.opacity = '0';
      el.style.transform = 'translateX(20px)';
      el.style.transition = 'all 0.2s ease-out';
      setTimeout(() => {
        if (el.parentNode) {
          el.parentNode.removeChild(el);
        }
      }, 200);
    }
  }

  // Update User UI
  function updateUserUI() {
    if (!currentUserId) {
      currentUserDisplay.textContent = 'secops_user';
      userAvatar.textContent = 'S';
      return;
    }
    currentUserDisplay.textContent = currentUserId;
    userAvatar.textContent = currentUserId.charAt(0).toUpperCase();
    localStorage.setItem('username', currentUserId);
  }

  // Fetch App Metadata
  async function fetchAppMetadata() {
    try {
      const res = await fetch(`${API_BASE_URL}/app_name`);
      if (res.ok) {
        const data = await res.json();
        if (data.app_name) {
          appTitle.textContent = data.app_name;
          document.title = data.app_name;
        }
      }
    } catch (e) {
      console.warn('Could not fetch app name:', e);
    }
  }

  // Fetch MCP Server Status Pills
  async function fetchMcpInfo() {
    try {
      const res = await fetch(`${API_BASE_URL}/info`);
      if (res.ok) {
        const data = await res.json();
        if (data.user && !currentUserId) {
          currentUserId = data.user;
          updateUserUI();
        }
        const mcp = data.tools || data.mcp_servers || {};
        updatePill(pillSecops, mcp.secops);
        updatePill(pillScc, mcp.scc);
        updatePill(pillGti, mcp.gti);
        updatePill(pillSoar, mcp.soar);
      }
    } catch (e) {
      console.warn('Could not fetch MCP server info:', e);
    }
  }

  function updatePill(pillEl, isEnabled) {
    if (!pillEl) return;
    const dot = pillEl.querySelector('.status-dot');
    if (dot) {
      if (isEnabled) {
        dot.classList.add('active');
        pillEl.title = 'Enabled and connected';
      } else {
        dot.classList.remove('active');
        pillEl.title = 'Disabled or not configured';
      }
    }
  }

  // Fetch / Initialize Session
  async function initSession(startNew = false) {
    try {
      let url = `${API_BASE_URL}/get_session`;
      if (currentUserId) {
        url += `?username=${encodeURIComponent(currentUserId)}`;
      }
      if (startNew) {
        url += (currentUserId ? '&' : '?') + 'start_new_session=Y';
      }
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      currentSessionId = data.session_id;
      if (data.user_id) {
        currentUserId = data.user_id;
        updateUserUI();
      }
      currentSessionDisplay.textContent = currentSessionId.slice(0, 8) + '...';
      currentSessionDisplay.title = currentSessionId;
      console.log('Active session initialized:', currentSessionId, 'User:', currentUserId);
    } catch (err) {
      console.error('Session initialization failed:', err);
      showToast('Could not initialize session with backend', 'error');
    }
  }

  // Safe Markdown Rendering with DOMPurify Sanitization
  function renderMarkdown(rawText) {
    if (window.marked && typeof window.marked.parse === 'function') {
      const rawHtml = window.marked.parse(rawText);
      if (window.DOMPurify && typeof window.DOMPurify.sanitize === 'function') {
        return window.DOMPurify.sanitize(rawHtml);
      }
      return rawHtml;
    }
    const div = document.createElement('div');
    div.textContent = rawText;
    return div.innerHTML;
  }

  // Append Message
  function appendMessage(text, sender, timeElapsed = null, timeDiff = null) {
    if (emptyState && emptyState.style.display !== 'none') {
      emptyState.style.display = 'none';
    }

    const row = document.createElement('div');
    row.className = `message-row ${sender}`;

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    avatar.textContent = sender === 'user' ? currentUserId.charAt(0).toUpperCase() : 'G';
    row.appendChild(avatar);

    const bodyWrap = document.createElement('div');
    bodyWrap.className = 'message-body-wrap';

    const headerInfo = document.createElement('div');
    headerInfo.className = 'message-header-info';
    const authorSpan = document.createElement('span');
    authorSpan.textContent = sender === 'user' ? currentUserId : 'Google SecOps Agent';
    headerInfo.appendChild(authorSpan);

    if (timeElapsed !== null) {
      const timeSpan = document.createElement('span');
      let timingStr = `${timeElapsed}ms`;
      if (timeDiff !== null && sender === 'agent') {
        timingStr += ` (${timeDiff}ms)`;
      }
      timeSpan.textContent = timingStr;
      headerInfo.appendChild(timeSpan);
    }

    bodyWrap.appendChild(headerInfo);

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';

    if (sender === 'agent') {
      bubble.innerHTML = renderMarkdown(text);
      addCopyButtonsToPre(bubble);
    } else {
      bubble.textContent = text;
    }

    bodyWrap.appendChild(bubble);
    row.appendChild(bodyWrap);

    messagesContainer.appendChild(row);
    scrollToBottom();
    return bubble;
  }

  // Code Copy Buttons
  function addCopyButtonsToPre(container) {
    const preBlocks = container.querySelectorAll('pre');
    preBlocks.forEach((pre) => {
      if (pre.querySelector('.code-copy-btn')) return;
      const code = pre.querySelector('code');
      const copyBtn = document.createElement('button');
      copyBtn.className = 'code-copy-btn';
      copyBtn.textContent = 'Copy';
      copyBtn.onclick = async () => {
        try {
          const textToCopy = code ? code.innerText : pre.innerText;
          await navigator.clipboard.writeText(textToCopy);
          copyBtn.textContent = 'Copied!';
          setTimeout(() => {
            copyBtn.textContent = 'Copy';
          }, 1800);
        } catch (e) {
          showToast('Failed to copy code to clipboard', 'warning');
        }
      };
      pre.appendChild(copyBtn);
    });
  }

  function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Stream Response Handler
  async function handleUserSubmit() {
    const prompt = chatTextarea.value.trim();
    if (!prompt || isStreaming) return;

    if (!currentSessionId) {
      await initSession();
      if (!currentSessionId) {
        showToast('Waiting for session initialization. Try again in a moment.', 'warning');
        return;
      }
    }

    appendMessage(prompt, 'user', 0);
    chatTextarea.value = '';
    autoResizeTextarea();

    // Prepare Agent Streaming Container
    isStreaming = true;
    sendBtn.style.display = 'none';
    cancelBtn.style.display = 'flex';
    requestStartTime = Date.now();
    lastChunkTime = requestStartTime;

    const streamRow = document.createElement('div');
    streamRow.className = 'message-row agent';

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    avatar.textContent = 'G';
    streamRow.appendChild(avatar);

    const bodyWrap = document.createElement('div');
    bodyWrap.className = 'message-body-wrap';

    const headerInfo = document.createElement('div');
    headerInfo.className = 'message-header-info';
    headerInfo.innerHTML = '<span class="streaming-pulse"></span><span>Investigating...</span>';
    bodyWrap.appendChild(headerInfo);

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.innerHTML = '<em>Analyzing security telemetry...</em>';
    bodyWrap.appendChild(bubble);

    streamRow.appendChild(bodyWrap);
    messagesContainer.appendChild(streamRow);
    scrollToBottom();

    activeAbortController = new AbortController();
    let accumulatedText = '';

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream, application/json',
        },
        body: JSON.stringify({
          session_id: currentSessionId,
          user_id: currentUserId,
          message: prompt,
        }),
        signal: activeAbortController.signal,
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        let boundary = buffer.indexOf('\n\n');

        while (boundary !== -1) {
          const chunk = buffer.substring(0, boundary);
          buffer = buffer.substring(boundary + 2);

          if (chunk.startsWith('data: ')) {
            try {
              const data = JSON.parse(chunk.substring(6));
              const now = Date.now();
              const timeElapsed = now - requestStartTime;
              const timeDiff = now - lastChunkTime;
              lastChunkTime = now;

              if (data.last_msg && data.text === 'Stream finished.') {
                headerInfo.innerHTML = `<span>Google SecOps Agent</span><span>${timeElapsed}ms</span>`;
                reader.cancel();
                break;
              } else if (data.text) {
                const isBlock = data.event_type === 'tool_call' ||
                                data.event_type === 'tool_response' ||
                                data.event_type === 'error' ||
                                (!data.event_type && (data.text.startsWith('[Tool]') || data.text.startsWith('[Error]') || data.text.startsWith('[Warning]')));

                if (!accumulatedText) {
                  accumulatedText = data.text;
                } else if (isBlock) {
                  accumulatedText += '\n\n' + data.text;
                } else {
                  accumulatedText += data.text;
                }
                bubble.innerHTML = renderMarkdown(accumulatedText);
                addCopyButtonsToPre(bubble);
                headerInfo.innerHTML = `<span class="streaming-pulse"></span><span>${timeElapsed}ms (${timeDiff}ms)</span>`;
                scrollToBottom();
              }
            } catch (jsonErr) {
              console.warn('Could not parse SSE chunk:', chunk, jsonErr);
            }
          }
          boundary = buffer.indexOf('\n\n');
        }
      }

      const totalTime = Date.now() - requestStartTime;
      headerInfo.innerHTML = `<span>Google SecOps Agent</span><span>${totalTime}ms</span>`;
    } catch (err) {
      if (err.name === 'AbortError') {
        headerInfo.innerHTML = '<span>Google SecOps Agent</span><span style="color: var(--color-warning);">(Cancelled)</span>';
        showToast('Investigation query cancelled', 'info');
      } else {
        console.error('Chat error:', err);
        headerInfo.innerHTML = '<span>Google SecOps Agent</span><span style="color: var(--color-danger);">(Error)</span>';
        bubble.innerHTML = `<span style="color: var(--color-danger);">Failed to get response from server: ${err.message}</span>`;
        showToast(`Request failed: ${err.message}`, 'error');
      }
    } finally {
      isStreaming = false;
      activeAbortController = null;
      sendBtn.style.display = 'flex';
      cancelBtn.style.display = 'none';
      scrollToBottom();
      chatTextarea.focus();
    }
  }

  // Cancel Streaming
  function cancelStreaming() {
    if (activeAbortController) {
      activeAbortController.abort();
    }
  }

  // Auto-resize Textarea
  function autoResizeTextarea() {
    chatTextarea.style.height = 'auto';
    chatTextarea.style.height = Math.min(chatTextarea.scrollHeight, 160) + 'px';
  }

  // Modal Handling
  function openUserModal() {
    usernameInput.value = currentUserId;
    userModal.style.display = 'flex';
    usernameInput.focus();
  }

  function closeUserModal() {
    userModal.style.display = 'none';
  }

  function saveUser() {
    const newName = usernameInput.value.trim();
    if (!newName) {
      showToast('Username cannot be empty', 'warning');
      return;
    }
    currentUserId = newName;
    updateUserUI();
    closeUserModal();
    initSession(true);
    showToast(`Active user set to: ${currentUserId}`, 'success');
  }

  // Event Listeners
  sendBtn.addEventListener('click', handleUserSubmit);
  cancelBtn.addEventListener('click', cancelStreaming);

  chatTextarea.addEventListener('input', autoResizeTextarea);
  chatTextarea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleUserSubmit();
    }
  });

  themeToggleBtn.addEventListener('click', toggleTheme);

  userChip.addEventListener('click', openUserModal);
  saveUserBtn.addEventListener('click', saveUser);
  cancelUserBtn.addEventListener('click', closeUserModal);
  userModal.addEventListener('click', (e) => {
    if (e.target === userModal) closeUserModal();
  });

  newInvestigationBtn.addEventListener('click', () => {
    messagesContainer.innerHTML = '';
    if (emptyState) {
      emptyState.style.display = 'flex';
      messagesContainer.appendChild(emptyState);
    }
    initSession(true);
    showToast('Started a new investigation session', 'info');
    chatTextarea.focus();
  });

  // Quick Prompt Cards
  document.querySelectorAll('.quick-prompt-card').forEach((card) => {
    card.addEventListener('click', () => {
      const prompt = card.getAttribute('data-prompt');
      if (prompt) {
        chatTextarea.value = prompt;
        autoResizeTextarea();
        chatTextarea.focus();
      }
    });
  });

  // Initialization
  initTheme();
  updateUserUI();
  fetchAppMetadata();
  fetchMcpInfo();
  initSession(false);
  autoResizeTextarea();
});
