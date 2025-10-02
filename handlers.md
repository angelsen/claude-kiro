```
HANDLER CONFIGURATION

Available Handlers: CONFIRMATION, PYTHON, CLAUDE
Actions: auto, ask, never, auto-ask, ask-ask
Timeout: 2s, 5s, 10s, 30s
Line Endings: lf (Unix), crlf (Windows), cr (Mac Classic)

Note: CONFIRMATION handler manages SSH connections and all processes
on systems without /proc (macOS, BSD).

Syntax:
# HANDLER_NAME
## Group Name (action, timeout)        # Unix/Linux (default)
## Group Name (action, timeout, crlf)  # Windows servers
- pattern
- ~disabled~
- pattern # comment

Actions:
- auto: Send automatically, wait for timeout
- ask: Ask before sending, wait for timeout
- never: Block command
- auto-ask: Send automatically, ask when done
- ask-ask: Ask before sending, ask when done

Example:
# CONFIRMATION
## Safe Commands (auto, 2s)
- ls
- pwd

## Windows Commands (auto, 2s, crlf)
- dir
- ipconfig

## Interactive Commands (auto-ask, 5s)  # Ask when done
- vim *
- nano *

## File Operations (ask, 5s)
- rm *
- cp *

## Dangerous (never)
- sudo *
- rm -rf *
```
