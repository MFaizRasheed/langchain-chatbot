# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run Streamlit web application
streamlit run app.py

# Run CLI chatbot
python main.py

# Run FastAPI backend (development)
uvicorn src.main:app --reload
```

## Architecture

### Application Entry Points

**`app.py` - Streamlit Web UI**
- Full-featured chat interface with sidebar settings
- Uses `st.session_state` for state persistence across reruns
- Real-time memory visualization and warnings

**`main.py` - CLI Chatbot**
- Terminal-based conversation interface
- Global `chat_history` list for conversation memory
- Simple turn-based memory management

**`src/main.py` - FastAPI Backend (WIP)**
- Basic REST API structure
- Currently provides health check and example endpoints

### LangChain + Ollama Integration Flow

```
User Input
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  ChatPromptTemplate                                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ ("system", "You are a helpful AI assistant.")         │  │
│  │ MessagesPlaceholder(variable_name="chat_history")     │  │
│  │ ("human", "{question}")                               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
    │
    │ Formatted Prompt (str)
    ▼
┌─────────────────────────────────────────────────────────────┐
│  ChatOllama (LangChain → Ollama Bridge)                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ - model: "minimax-m2.5:cloud" (or configured model)   │  │
│  │ - temperature: 0.7 (creativity control)               │  │
│  │ - Sends HTTP request to Ollama API (localhost:11434)  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
    │
    │ Ollama API Response
    ▼
┌─────────────────────────────────────────────────────────────┐
│  StrOutputParser                                            │
│  - Extracts text content from LLM response                  │
│  - Returns clean string for display                         │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
AI Response (displayed to user)
```

### LangChain Components

| Component | Purpose |
|-----------|---------|
| `ChatOllama` | LLM wrapper that connects to Ollama API for local/cloud model inference |
| `ChatPromptTemplate` | Structures conversation with system prompt, message history placeholder, and user input |
| `MessagesPlaceholder` | Injects `chat_history` (list of HumanMessage/AIMessage) into prompt |
| `StrOutputParser` | Parses LLM response to extract plain text |

### Ollama Connection

- Default model: `minimax-m2.5:cloud`
- Ollama API endpoint: `http://localhost:11434` (default)
- Uses `langchain-ollama` package as bridge between LangChain and Ollama

### Conversation Memory Pattern

```
turns_used = len(chat_history) // 2  # Each turn = 1 HumanMessage + 1 AIMessage
remaining = max_turns - turns_used

Memory flow:
1. Check if turns_used >= max_turns → warn user
2. Invoke chain with chat_history
3. Append HumanMessage(question) to chat_history
4. Append AIMessage(response) to chat_history
5. If remaining <= 2, append warning to response
```

### Streamlit State Management

```python
# Initialized once per session, persisted across reruns
st.session_state.chat_history  # [HumanMessage, AIMessage, ...]
st.session_state.llm           # ChatOllama instance
st.session_state.chain         # prompt | llm | parser pipeline
st.session_state.messages      # [{"role": "user"/"assistant", "content": "..."}]
st.session_state.max_turns     # Conversation memory limit
```

## Module Structure (`src/`)

```
src/
├── api/          # FastAPI route handlers (WIP)
├── config/       # Settings, environment config
├── core/         # Core utilities, shared logic
├── models/       # Pydantic models, data schemas
├── providers/    # LLM provider integrations (Ollama wrapper)
└── services/     # Business logic, chat services
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_NAME` | Ollama model identifier | `minimax-m2.5:cloud` |
| `TEMPERATURE` | LLM temperature (0.0-1.0) | `0.7` |
| `MAX_TURNS` | Max conversation turns to remember | `5` |

## Key Patterns

- **Chain composition**: Use `|` operator to compose `prompt | llm | parser`
- **Message types**: `HumanMessage` for user input, `AIMessage` for responses
- **Session persistence**: Streamlit reruns require `st.session_state` for all mutable state
- **Turn-based memory**: Count pairs of messages, not individual messages
