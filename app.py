import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
<style>
    /* Main chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }

    /* Message bubbles */
    .stChatMessage {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }

    /* User message styling */
    [data-testid="stChatMessage-user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }

    /* Assistant message styling */
    [data-testid="stChatMessage-assistant"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #1a1a2e;
        margin-right: 2rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Custom button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* Title styling */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    /* Status indicator */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }

    .status-online {
        background: #10b981;
        box-shadow: 0 0 8px #10b981;
    }

    .status-warning {
        background: #f59e0b;
        box-shadow: 0 0 8px #f59e0b;
    }

    /* Memory indicator */
    .memory-bar {
        height: 6px;
        border-radius: 3px;
        background: #e5e7eb;
        margin-top: 8px;
        overflow: hidden;
    }

    .memory-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 0.3s ease;
    }

    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 24px;
        padding: 12px 20px;
        border: 2px solid #e5e7eb;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "max_turns" not in st.session_state:
    st.session_state.max_turns = 5
if "llm" not in st.session_state:
    st.session_state.llm = ChatOllama(
        model="minimax-m2.5:cloud",
        temperature=0.7,
    )
if "chain" not in st.session_state:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful AI assistant."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )
    st.session_state.chain = prompt | st.session_state.llm | StrOutputParser()
if "messages" not in st.session_state:
    st.session_state.messages = []


def get_remaining_turns():
    """Calculate remaining turns based on current chat history"""
    return st.session_state.max_turns - (len(st.session_state.chat_history) // 2)


def get_memory_percentage():
    """Get the percentage of memory used"""
    used = len(st.session_state.chat_history) // 2
    return (used / st.session_state.max_turns) * 100


def get_memory_color():
    """Get color based on remaining turns"""
    remaining = get_remaining_turns()
    if remaining <= 1:
        return "#ef4444"  # Red
    elif remaining <= 2:
        return "#f59e0b"  # Orange
    return "#10b981"  # Green


def clear_chat():
    """Clear chat history"""
    st.session_state.chat_history = []
    st.session_state.messages = []


# Sidebar settings
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    # Model selection
    st.markdown("### Model")
    model_name = st.text_input(
        "Model Name", value="minimax-m2.5:cloud", help="Enter the Ollama model name"
    )

    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness in responses",
    )

    # Max turns
    max_turns = st.slider(
        "Conversation Memory",
        min_value=3,
        max_value=20,
        value=5,
        step=1,
        help="Number of conversation turns to remember",
    )

    # Apply settings button
    if st.button("Apply Settings", use_container_width=True):
        st.session_state.llm = ChatOllama(
            model=model_name,
            temperature=temperature,
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful AI assistant."),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        st.session_state.chain = prompt | st.session_state.llm | StrOutputParser()
        st.session_state.max_turns = max_turns
        st.success("Settings applied!")

    st.markdown("---")

    # Memory status
    st.markdown("### 💾 Memory Status")
    remaining = get_remaining_turns()
    memory_pct = get_memory_percentage()
    memory_color = get_memory_color()

    col1, col2 = st.columns([1, 2])
    with col1:
        status_class = "status-warning" if remaining <= 2 else "status-online"
        st.markdown(
            f'<span class="status-indicator {status_class}"></span>'
            f"{remaining} turns left",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="memory-bar">
                <div class="memory-fill" style="width: {memory_pct}%; background: {memory_color};"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Action buttons
    st.markdown("### 🗑️ Actions")
    if st.button("Clear Chat History", use_container_width=True):
        clear_chat()
        st.rerun()

    st.markdown("---")

    # Info
    st.markdown("### ℹ️ Tips")
    st.markdown("""
    - Type **'clear'** to reset chat
    - Adjust temperature for creativity
    - Higher memory = more context
    """)


# Main content
st.markdown('<div class="main-title">🤖 AI Chatbot</div>', unsafe_allow_html=True)

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    if not st.session_state.messages:
        st.info("👋 Start a conversation! Type your message below.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here...", key="chat_input"):
    # Handle clear command
    if prompt.lower().strip() == "clear":
        clear_chat()
        st.rerun()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check memory limit
    remaining = get_remaining_turns()

    if remaining <= 0:
        warning_msg = (
            "⚠️ Context window is full. The AI may not follow your previous thread properly. "
            "Please type 'clear' for a new chat."
        )
        st.session_state.messages.append({"role": "assistant", "content": warning_msg})
        with st.chat_message("assistant"):
            st.markdown(warning_msg)
    else:
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Invoke the chain
                    response = st.session_state.chain.invoke(
                        {
                            "question": prompt,
                            "chat_history": st.session_state.chat_history,
                        }
                    )

                    # Add warning if running low on memory
                    if remaining <= 2:
                        response += (
                            f"\n\n⚠️ **{remaining} turn(s) left before memory resets.**"
                        )

                    # Store in history
                    st.session_state.chat_history.append(HumanMessage(content=prompt))
                    st.session_state.chat_history.append(AIMessage(content=response))

                    # Display response
                    st.markdown(response)

                    # Add to messages
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )

# Auto-scroll to bottom
if st.session_state.messages:
    st.markdown(
        "<script>window.scrollTo(0, document.body.scrollHeight);</script>",
        unsafe_allow_html=True,
    )
