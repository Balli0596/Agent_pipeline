# AI Agent with Tools — Gemini + LangChain

An AI-powered chatbot that understands natural-language queries and dynamically selects Python tools to retrieve weather information and stock prices. Built with Google Gemini, LangChain Agents, FastAPI, and React.

## Features

- **Intelligent tool routing:** Gemini selects the appropriate Python tool based on user intent.
- **Weather information:** Retrieves current weather conditions for a specified city using Open-Meteo.
- **Stock prices:** Retrieves the latest available closing price for a stock using `yfinance`.
- **Interactive chatbot:** React-based interface with suggested prompts, chat messages, and loading states.
- **REST API:** FastAPI connects the frontend to the agent.
- **Modular architecture:** Agent logic, tools, API integrations, and frontend are separated.
- **Error handling:** Handles invalid requests and external service failures.

## Architecture

```text
User
 |
 v
React + TypeScript Frontend
 |
 | POST /api/chat
 v
FastAPI Backend
 |
 v
LangChain Agent + Google Gemini
 |
 |-- Weather Tool
 |    |-- Open-Meteo Geocoding API
 |    |-- Open-Meteo Weather API
 |
 |-- Stock Tool
      |-- yfinance
      |-- Yahoo Finance data
 |
 v
Tool Result → Gemini → Final Response
 |
 v
Chat Interface
```

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python, TypeScript |
| LLM | Google Gemini |
| Agent Framework | LangChain |
| Backend API | FastAPI |
| Frontend | React, Vite |
| Weather Data | Open-Meteo |
| Stock Data | yfinance |
| Configuration | python-dotenv |
| Testing | pytest |

## Project Structure

```text
ai-agent-tools/
├── agent/
│   ├── __init__.py
│   ├── controller.py
│   └── tool_registry.py
├── tools/
│   ├── __init__.py
│   ├── weather_tool.py
│   └── stock_tool.py
├── tests/
│   └── test_tools.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.tsx
│   ├── package.json
│   └── index.html
├── api.py
├── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

Install the following before running the project:

- Python 3.10 or newer
- Node.js and npm
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
- Internet access for external APIs

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Balli0596/Agent_pipeline
cd ai-agent-tools
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Set up the Python backend

Create and activate a virtual environment on Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash
```

Use a Gemini model that is available to your API key. Never commit your `.env` file or expose your API key publicly.

### 4. Start the FastAPI backend

From the project root:

```bash
uvicorn api:app --reload
```

Backend URL: `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

Health check: `http://127.0.0.1:8000/api/health`

### 5. Start the React frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the frontend URL printed by Vite, normally:

`http://localhost:5173`

Keep both the backend and frontend terminals running while using the application.

## API Endpoints

### Health Check

`GET /api/health`

Example response:

```json
{
  "status": "ok",
  "service": "AI Agent API"
}
```

### Chat

`POST /api/chat`

Request:

```json
{
  "message": "What is the current weather in Jaipur?"
}
```

Response:

```json
{
  "reply": "The current weather in Jaipur is ..."
}
```

The actual response depends on the live API data and Gemini's generated answer.

## Example Queries

**Weather**

- What is the current weather in Jaipur?
- Compare the weather in Jaipur and Mumbai.

**Stocks**

- What is the latest closing price of TCS?
- What is the latest closing price of Reliance Industries?

For Indian stocks, symbols such as `TCS.NS` and `RELIANCE.NS` are used with Yahoo Finance.

**General questions**

- What is the difference between AI and machine learning?

The agent can answer general questions without calling the weather or stock tools.

## Running Tests

From the project root:

```bash
python -m pytest tests/ -v
```

Tests that call external services require an internet connection and can be affected by provider outages or rate limits.

## How Tool Calling Works

1. The user submits a natural-language query.
2. Gemini determines whether a tool is required.
3. LangChain executes the selected registered Python function.
4. The tool retrieves data from its external provider.
5. LangChain returns the tool result to Gemini.
6. Gemini generates a natural-language response.
7. FastAPI returns the response to the React interface.

Gemini selects the tool; Python executes it. The model does not directly execute arbitrary Python code.

## Important Notes

- Weather data depends on Open-Meteo availability.
- `yfinance` is an unofficial interface to Yahoo Finance data and may be subject to rate limits or data availability restrictions.
- Stock responses currently represent the latest available closing price, not necessarily a live intraday price.
- The current chatbot keeps conversation messages in frontend state; persistent chat history and multi-turn backend memory are not implemented.
- The current CORS configuration permits the local Vite development origin. Production deployments require appropriate origin configuration and additional security measures.
- Do not expose API keys in frontend code or commit them to version control.

## Future Improvements

- Persistent conversation history and session-based memory
- Streaming responses
- Visible tool execution indicators
- Better validation and automated tests for tool routing
- Authentication, rate limiting, and production deployment
- Additional tools and data sources
---
