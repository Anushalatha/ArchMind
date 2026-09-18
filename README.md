# ArchMind - AI System Architect

> An LLM-powered system architecture assistant that transforms natural-language product ideas into structured technical architecture proposals.

## Overview

ArchMind helps developers and product teams move from a high-level product idea to an initial technical architecture.

Users describe what they want to build, configure the expected application type and scale, and receive a structured architecture containing system components, APIs, database entities, AI components, security considerations, scalability considerations, and architectural risks.

The application uses an LLM as an architecture-generation component rather than as a simple conversational chatbot.

## Key Features

- Natural-language system requirements
- LLM-powered architecture generation
- Structured JSON output
- Pydantic-based validation
- Component architecture recommendations
- REST API endpoint suggestions
- Database entity suggestions
- AI component identification
- Security and scalability considerations
- Architecture risks and trade-offs
- Separate architecture critique
- Streamlit-based interactive interface
- Environment-based API key management
- Error handling for invalid or failed LLM responses

## Architecture

```text
User
   |
   v
Streamlit Interface
   |
   v
Prompt Builder
   |
   v
LLM API
   |
   v
Structured JSON
   |
   v
Pydantic Validation
   |
   v
Architecture Service
   |
   v
Streamlit Visualization
```

## Example Workflow

```text
Product Idea
       |
       v
Requirements Analysis
       |
       v
Architecture Generation
       |
       v
Component Identification
       |
       v
API Design
       |
       v
Database Design
       |
       v
AI Component Design
       |
       v
Security and Scalability Analysis
```

## Tech Stack

- Python
- Streamlit
- Groq or OpenAI-compatible API
- OpenAI Python SDK
- Pydantic
- python-dotenv

## Project Structure

```text
ai-system-architect/
|
├── app.py
├── requirements.txt
├── .gitignore
|
├── core/
|   ├── llm.py
|   ├── prompts.py
|   └── schemas.py
|
└── services/
      ├── architect.py
      └── critic.py
```

## Setup

### 1. Clone the repository

```powershell
git clone <your-repository-url>
cd ai-system-architect
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the API key

Create a local `.env` file in the project root. For Groq:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

OpenAI is also supported:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Never commit `.env` or expose API keys. The file is excluded by `.gitignore`.

### 5. Run the application

```powershell
streamlit run app.py
```

The application will be available through the Streamlit development server, usually at `http://localhost:8501`.

## Example Input

```text
Build an AI-powered learning platform where students can upload study materials,
ask questions, generate quizzes, track their learning progress, and receive
personalized recommendations.
```

## Example Output

ArchMind generates structured sections such as:

- System Overview
- Functional Requirements
- Non-Functional Requirements
- Architecture Components
- API Endpoints
- Database Entities
- AI Components
- Security Considerations
- Scalability Considerations
- Risks and Trade-offs

## Engineering Approach

A key design decision in ArchMind is separating the LLM from the application logic.

Instead of treating the LLM response as arbitrary text, the application converts the model response into a structured representation and validates it before displaying the architecture.

```text
LLM
 |
 v
Structured Output
 |
 v
Validation
 |
 v
Application Logic
 |
 v
UI
```

This approach makes the application easier to extend with additional capabilities such as architecture evaluation, document-based knowledge retrieval, automated API validation, and AI agents.

## Future Improvements

Planned improvements include:

- Architecture comparison
- Architecture diagrams
- Export to Markdown or PDF
- Architecture version history
- RAG-based architecture knowledge
- Technical documentation retrieval
- Tool-using architecture agent
- FastAPI backend
- Evaluation and monitoring
- Docker deployment

## Project Status

**Version:** 1.0 - MVP

The current version focuses on LLM integration, structured architecture generation, validation, interactive visualization, and architecture critique.

## Author

Anusha
