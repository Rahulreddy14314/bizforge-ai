from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import ai_services

app = FastAPI(title="BizForge API")

# Setup CORS for frontend compilation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BrandRequest(BaseModel):
    industry: str
    keywords: str
    tone: str
    language: str

class IdeaRequest(BaseModel):
    keywords: str

class ContentRequest(BaseModel):
    product: str
    tone: str
    content_type: str

class SentimentRequest(BaseModel):
    text: str

class ColorRequest(BaseModel):
    industry: str
    vibes: str

class LogoRequest(BaseModel):
    brand_name: str
    industry: str
    style: str

class ChatEntry(BaseModel):
    user: str
    assistant: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatEntry]

@app.post("/api/generate-brand")
async def generate_brand(req: BrandRequest):
    result = ai_services.generate_brand_names(req.industry, req.keywords, req.tone, req.language)
    names = [n.strip() for n in result.split('\n') if n.strip()]
    return {"names": names}

@app.post("/api/generate-idea")
async def generate_idea(req: IdeaRequest):
    idea = ai_services.generate_startup_idea(req.keywords)
    return {"idea": idea}

@app.post("/api/generate-content")
async def generate_content(req: ContentRequest):
    content = ai_services.generate_marketing_content(req.product, req.tone, req.content_type)
    return {"content": content}

@app.post("/api/analyze-sentiment")
async def analyze_sentiment(req: SentimentRequest):
    result = ai_services.analyze_sentiment(req.text)
    return result

@app.post("/api/get-colors")
async def get_colors(req: ColorRequest):
    result = ai_services.get_color_palette(req.industry, req.vibes)
    return result

@app.post("/api/generate-logo")
async def generate_logo(req: LogoRequest):
    prompt = ai_services.generate_logo_prompt(req.brand_name, req.industry, req.style)
    image_data = ai_services.generate_logo(prompt)
    if not image_data:
        return {"prompt": prompt, "error": "Logo generation failed. Ensure HF API key is set or try again later.", "image_data": ""}
    return {"prompt": prompt, "image_data": image_data}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    history_dict = [{"user": h.user, "assistant": h.assistant} for h in req.history]
    reply = ai_services.chat_with_ai(req.message, history_dict)
    return {"reply": reply}

@app.post("/api/transcribe-voice")
async def transcribe_voice(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    text = ai_services.transcribe_voice(audio_bytes)
    return {"text": text}

@app.get("/")
def health_check():
    return {"status": "ok", "message": "BizForge API is running successfully"}
