# LangChain Chatbot

A modern AI-powered chatbot application built with LangChain, Ollama, and Streamlit. Features both a web-based UI and a command-line interface for interactive conversations with local LLM models.

## Features

- **Dual Interface Options**
  - 🖥️ **Streamlit Web UI** - Beautiful, responsive web interface with modern styling
  - 💻 **CLI Interface** - Simple terminal-based chat interface

- **Conversation Management**
  - Configurable conversation memory (configurable turns)
  - Automatic memory limit warnings
  - Chat history reset functionality

- **Customizable Settings**
  - Model selection (supports Ollama models)
  - Temperature control for response creativity
  - Adjustable conversation memory size

- **Modern UI Components** (Streamlit)
  - Gradient-styled chat bubbles
  - Real-time memory status indicator
  - Animated progress bars
  - Responsive sidebar with settings

## Tech Stack

- **Core Framework**: LangChain 1.2+
- **LLM Provider**: Ollama (supports local and cloud models)
- **Web UI**: Streamlit
- **API Backend**: FastAPI (in development)
- **Environment Management**: python-dotenv
- **Package Manager**: uv

## Prerequisites

- Python 3.11.14 or higher
- [Ollama](https://ollama.ai) installed and running
- uv package manager (recommended) or pip

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd langchain-chatbot

# Install dependencies
uv sync
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd langchain-chatbot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
MODEL_NAME=minimax-m2.5:cloud
TEMPERATURE=0.7
MAX_TURNS=5
```

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_NAME` | Ollama model to use | `minimax-m2.5:cloud` |
| `TEMPERATURE` | Response creativity (0.0-1.0) | `0.7` |
| `MAX_TURNS` | Conversation memory size | `5` |

## Usage

### Streamlit Web Application

Launch the web-based chatbot interface:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

**Web UI Features:**
- Adjust temperature slider for response creativity
- Change the Ollama model dynamically
- Configure conversation memory size
- View real-time memory status
- Clear chat history with one click

### Command-Line Interface

Run the CLI chatbot:

```bash
python main.py
```

**CLI Commands:**
- `quit` - Exit the chatbot
- `clear` - Reset conversation history
- Type any message to chat with the AI

## Project Structure

```
langchain-chatbot/
├── app.py                 # Streamlit web application
├── main.py                # CLI chatbot interface
├── pyproject.toml         # Project configuration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .env.example           # Example environment file
└── src/                   # Source modules (in development)
    ├── api/               # API endpoints
    ├── config/            # Configuration modules
    ├── core/              # Core functionality
    ├── models/            # Data models
    ├── providers/         # LLM providers
    └── services/          # Business logic services
```

## API Development (Work in Progress)

The `src/` directory contains a FastAPI-based backend structure currently under development:

```bash
# Run the FastAPI server (development)
uvicorn src.main:app --reload
```

Available endpoints:
- `GET /` - Health check
- `GET /items/{item_id}` - Example endpoint

## Available Ollama Models

You can use any Ollama-supported model. Some popular options:

```bash
# Pull a model
ollama pull llama2
ollama pull mistral
ollama pull codellama

# List available models
ollama list
```

## Troubleshooting

### Ollama Connection Error

Ensure Ollama is running:
```bash
ollama serve
```

### Model Not Found

Pull the required model:
```bash
ollama pull minimax-m2.5:cloud
```

### Import Errors

Reinstall dependencies:
```bash
uv sync --force
```

## Development

### Setting Up Development Environment

```bash
# Install with dev dependencies
uv sync --dev

# Run tests (when available)
pytest
```

### Code Style

This project follows Python PEP 8 style guidelines.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [LangChain](https://python.langchain.com/) - LLM orchestration framework
- [Ollama](https://ollama.ai/) - Local LLM runner
- [Streamlit](https://streamlit.io/) - Web application framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
