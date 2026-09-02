---
name: subagent
description: Use when running, coordinating, monitoring, or managing parallel Antigravity (agy) subagent tasks in detached tmux sessions or split panes
---

# Antigravity (agy) Subagent Manager

Orchestrates multiple parallel Antigravity (`agy`) CLI instances using `tmux` sessions. Subagents persist across exits, run background tasks or independent research, and can be queried or controlled asynchronously.

## Quick Reference

| Command | Action | Key Flags / Usage |
| :--- | :--- | :--- |
| `spawn` | Launch new subagent session | `--name=<name> --prompt="<prompt>" [--model=<model>]` |
| `spawn-split` | Launch subagent in split pane | `--name=<name> --prompt="<prompt>" [--vertical=true] [--size=50]` |
| `send` | Send prompt or command to subagent | `--name=<name> --message="<msg>"` |
| `get-output` | Retrieve output from subagent | `--name=<name> [--lines=50] [--all=true]` |
| `status` | Check session health, PID, and output | `--name=<name>` |
| `list` | List active subagent sessions | `[--format=detailed]` |
| `broadcast` | Send message to multiple subagents | `--names="agent1,agent2" --message="<msg>"` |
| `attach` | View interactive session | `tmux attach-session -t <name>` |
| `kill` | Terminate subagent session | `--name=<name>` |

---

## Subcommand Workflows

### 1. `spawn`
Starts a detached tmux session running `bash`, launches `agy`, waits for initialization, and submits the initial prompt.

```bash
# 1. Create detached tmux session
tmux new-session -d -s "<name>" bash

# 2. Launch agy in session
tmux send-keys -t "<name>" "agy" C-m

# 3. Wait for agy startup sequence (banner, tips, model connection)
sleep 5

# 4. Submit prompt (agy submits on single Enter)
tmux send-keys -t "<name>" -l "<prompt>"
tmux send-keys -t "<name>" C-m

# 5. Confirm session is alive
tmux list-sessions | grep "<name>"
```

*(If `--model` is specified, launch `agy --model <model>`)*

### 2. `spawn-split`
Spawns a subagent inside a split pane in the current tmux window using non-interactive print mode (`agy -p`).

```bash
# Horizontal (default) or Vertical (-h) split
tmux split-window -v -p 50 "agy -p '<prompt>'"

# Tag pane for identification
tmux select-pane -T "<name>"
```

### 3. `send`
Sends a prompt, shell command, or slash command to a running subagent session.

```bash
# For shell commands starting with '!':
tmux send-keys -t "<name>" "<command>" C-m

# For regular text prompts or slash commands:
tmux send-keys -t "<name>" -l "<message>"
tmux send-keys -t "<name>" C-m
```

### 4. `get-output`
Captures text lines from the target session's scrollback buffer.

```bash
# Last N lines (default 50):
tmux capture-pane -t "<name>" -p -S -50

# Entire available buffer:
tmux capture-pane -t "<name>" -p -S -
```

### 5. `status`
Inspects session existence, pane PID, running command, and recent output snippet.

```bash
# Verify session exists
tmux has-session -t "<name>" 2>/dev/null && echo "✓ Session '<name>' exists" || echo "✗ Session '<name>' not found"

# Show session details
tmux list-sessions -F "#{session_name}: #{session_windows} windows, created #{session_created_string}" | grep "<name>"

# Show running process & PID
tmux list-panes -t "<name>" -F "Pane: #{pane_current_command} (PID: #{pane_pid})" 2>/dev/null

# Capture last 10 lines
tmux capture-pane -t "<name>" -p -S -10 2>/dev/null
```

### 6. `list`
Lists active tmux sessions.

```bash
# Simple
tmux list-sessions 2>/dev/null || echo "No active subagents"

# Detailed
tmux list-sessions -F "Session: #{session_name} | Created: #{session_created_string} | Windows: #{session_windows} | Attached: #{session_attached}" 2>/dev/null
```

### 7. `broadcast`
Iterates over a comma-separated list of session names and sends the message to each.

```bash
for session in $(echo "<names>" | tr "," "\n"); do
  tmux send-keys -t "$session" -l "<message>" 2>/dev/null && tmux send-keys -t "$session" C-m 2>/dev/null && echo "Sent to $session" || echo "Failed to send to $session"
done
```

### 8. `attach`
Attach to view and interact with the session directly in your terminal:

```bash
tmux attach-session -t "<name>"
```
> **Detach Shortcut**: Press `Ctrl+B`, then `D` to detach and return to your parent terminal.

### 9. `kill`
Terminates the specified tmux session.

```bash
tmux kill-session -t "<name>" && echo "Subagent '<name>' terminated"
```

---

## Tips & Operational Notes
- Subagents run as persistent processes; always terminate unused sessions with `kill` to release system resources.
- In Antigravity CLI (`agy`), a single Enter (`C-m`) submits prompts. Do not send double Enter (`C-m C-m`).
- Use `-l` with `tmux send-keys` when sending prompt text to prevent tmux from interpreting special characters or key bindings.
