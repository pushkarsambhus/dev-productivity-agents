# Gmail AI Agent

A local CLI tool that connects to your Gmail and uses Claude to manage your inbox — read, summarize, reply, and compose emails on your behalf.

---

## Features

- **List & search** emails with Gmail query syntax
- **Read** full email threads
- **AI summaries** — Claude summarizes any email or your whole inbox
- **AI-drafted replies** — Claude drafts a reply in context; you preview before sending
- **AI-composed emails** — describe what you want to say, Claude writes it
- **Inbox actions** — archive, trash, mark read/unread
- Both an **interactive shell** and standalone **CLI commands**

---

## Setup

### 1. Get Google OAuth credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use an existing one)
3. Enable the **Gmail API**: APIs & Services → Library → search "Gmail API" → Enable
4. Create OAuth credentials: APIs & Services → Credentials → Create Credentials → OAuth client ID
   - Application type: **Desktop app**
5. Download the JSON file and save it as `credentials.json` in this directory
6. Under **OAuth consent screen**, add your Gmail address as a test user

### 2. Set your Anthropic API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Add this to your `~/.zshrc` or `~/.bashrc` to make it permanent.

### 3. Install dependencies

```bash
cd gmail-ai-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. First run (OAuth flow)

The first time you run the tool, a browser window will open for Google sign-in. After you approve, a `token.json` is saved locally — you won't need to log in again.

---

## Usage

### Interactive shell (recommended)

```bash
python main.py
```

Shell commands:

| Command | Description |
|---|---|
| `list` | List inbox |
| `list from:boss@co.com` | List with Gmail search |
| `search unread` | Search emails |
| `read 1` | Read email #1 from last list |
| `reply 1` | AI-draft a reply to #1 |
| `compose` | AI-compose a new email |
| `summarize` | Summarize all listed emails |
| `summarize 1` | Summarize email #1 |
| `archive 1` | Archive #1 |
| `trash 1` | Move #1 to trash |
| `read-mark 1` | Mark #1 as read |
| `unread-mark 1` | Mark #1 as unread |
| `help` | Show all commands |
| `exit` | Quit |

### Standalone CLI commands

```bash
python main.py list                          # list inbox
python main.py list "from:github.com"        # list with query
python main.py search "subject:invoice"
python main.py read <message-id>
python main.py reply <message-id>
python main.py compose
python main.py summarize                     # summarize inbox
python main.py summarize <message-id>
python main.py archive <message-id>
python main.py trash <message-id>
```

---

## Safety

- **Replies and new emails always show a preview** before sending — you confirm, edit in `$EDITOR`, or cancel
- `credentials.json` and `token.json` are gitignored
- OAuth scopes: read, send, modify (no delete scope — trash moves to trash, not permanent delete)

---

## Files

```
gmail-ai-agent/
├── main.py           # CLI entry point + interactive shell
├── gmail_client.py   # Gmail API wrapper
├── ai_agent.py       # Claude integration
├── auth.py           # OAuth2 flow
├── requirements.txt
├── credentials.json  # ← you provide this (gitignored)
└── token.json        # ← auto-created on first login (gitignored)
```
