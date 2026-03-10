# BizForge - AI Powered Branding Suite

BizForge is a modern web application that helps startups, creators, and small businesses dynamically generate customized branding assets. With a FastAPI Python backend and an animated HTML/Vanilla JS frontend, BizForge serves as an all-in-one central hub for brand creation powered by powerful AI models like Llama 3.3, Stable Diffusion XL, IBM Granite, and Whisper.

## Project Structure

```text
BizForge/
│
├── backend/
│   ├── main.py            # FastAPI Application routes
│   ├── ai_services.py     # API mapping to Groq/HuggingFace Services
│   ├── requirements.txt   # Python Dependencies
│   └── .env               # Secrets/Keys Template
│
├── frontend/
│   ├── index.html         # Hero / Feature landing page
│   ├── branding.html      # Central dashboard with tabbed tools
│   ├── style.css          # Vanilla CSS styling with glassmorphism 
│   └── script.js          # JS integrating UI with Backend
│
└── README.md
```

## Features Complete

- **Brand Generator**: Ask for 10-20 brand names using industry input logic.
- **Logo Generator**: Convert a textual query into an SDXL Prompt & generated Image Output.
- **Marketing Content**: Convert products dynamically tailored towards target markets.
- **Color Palette Analyzer**: Return JSON HEX Codes corresponding to specific moods or industries.
- **Review Analyzer**: Output "Positive" / "Negative" / "Neutral" alongside rewritten PR safe responses.
- **AI Specialist Agent**: Talk to "IBM Granite" powered conversational assistant wrapper.
- **Voice Typing**: Use the Web Audio recording API to transcribe voice inputs into tool prompts automatically utilizing Groq.

## Prerequisites

- Python 3.9+
- A valid Groq Cloud API key (for Text & Audio generation)
- A valid Hugging Face API Token (for Vision & Chat generations)

## Installation Guide

### 1. Setup Backend Dependencies
Navigate to the `backend` folder and install dependencies via pip:

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate       # Windows
# source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

### 2. Configure Environment Secrets
Create a `.env` inside the `backend` folder (based on the provided template) and populate it with your environment variables:

```ini
HF_API_KEY=hf_your_huggingface_token
IBM_MODEL=ibm-granite/granite-4.0-h-350m

GROQ_API_KEY=gsk_your_groq_api_token
GROQ_MODEL=llama-3.3-70b-versatile
```

### 3. Start the Backend Server
Run Uvicorn inside the `backend` folder on localhost port `8000`:

```bash
uvicorn main:app --reload
```

*The API will now be listening locally at `http://localhost:8000`*

### 4. Open the Client Application
Due to browser CORS policies with vanilla JS fetching to localhost services, it is highly recommended you open the `frontend` folder files out of a simple server instance if native `file:///` URLs give issues:

```bash
cd ../frontend
# Run a simple Python http server
python -m http.server 8080
```

1. Navigate to http://localhost:8080/index.html to view the landing page.
2. Click "Get Started for Free" to launch the main application interface.
