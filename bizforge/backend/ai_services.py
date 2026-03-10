import os
import io
import requests
import json
import base64
import urllib.parse
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
IBM_MODEL = os.getenv("IBM_MODEL", "ibm-granite/granite-4.0-h-350m")

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def generate_brand_names(industry: str, keywords: str, tone: str, language: str) -> str:
    if not groq_client: return "Groq API key not configured.\nPlease add your GROQ_API_KEY to the .env file."
    
    prompt = f"Generate 10-20 creative brand names for a startup in the {industry} industry. Keywords: {keywords}. Tone: {tone}. Language: {language}. Return ONLY the list format, without any conversational preamble or postscript."
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert brand identity consultant."},
                {"role": "user", "content": prompt}
            ],
            model=GROQ_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def generate_marketing_content(product: str, tone: str, content_type: str) -> str:
    if not groq_client: return "Groq API key not configured."
    
    prompt = f"Generate a {content_type} for this product: '{product}'. Tone: {tone}. Be creative, targeted, and highly engaging."
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=GROQ_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def generate_startup_idea(keywords: str) -> str:
    if not groq_client: return "Groq API key not configured."
    
    prompt = f"Analyze these inputs/keywords: '{keywords}' and produce a creative startup idea. Example workflow: User Input -> 'Food + AI', AI Output -> 'An AI-powered diet planning startup that analyzes a user’s health data and recommends personalized meal plans.' Be concise, direct, and creative."
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert startup idea generator. Output only the startup idea itself without conversational filler."},
                {"role": "user", "content": prompt}
            ],
            model=GROQ_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_sentiment(text: str) -> dict:
    if not groq_client: 
        return {"sentiment": "Unknown", "confidence": "0%", "rewritten": "Groq API key not configured."}
        
    prompt = f"Analyze the sentiment of the following customer review/text: '{text}'. Return JSON with exactly these keys: 'sentiment' (Positive, Neutral, or Negative), 'confidence' (string like '95%'), and 'rewritten' (a politely rewritten version of the text if it's negative, or a marketing-enhanced version if positive/neutral). Return ONLY valid JSON."
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a Sentiment Analysis JSON API. Output strictly valid JSON and nothing else."},
                {"role": "user", "content": prompt}
            ],
            model=GROQ_MODEL,
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        print("Analyze sentiment error:", e)
        return {"sentiment": "Error", "confidence": "0%", "rewritten": "Failed to analyze text."}

def get_color_palette(industry: str, vibes: str) -> dict:
    if not groq_client: 
        return {"colors": ["#1A1A1A", "#FFFFFF", "#3B82F6", "#10B981", "#F59E0B"]}
        
    prompt = f"Generate a modern professional color palette of exactly 5 colors for a brand in the {industry} industry with this style/vibe: {vibes}. Return JSON with exactly a 'colors' key containing a list of 5 HEX code strings (e.g. ['#FFFFFF', ...]). Return ONLY JSON, no markdown formatting."
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a specialized color palette JSON API. Output exactly JSON and nothing else."},
                {"role": "user", "content": prompt}
            ],
            model=GROQ_MODEL,
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        print("Get color palette error:", e)
        return {"colors": ["#111827", "#F3F4F6", "#4F46E5", "#10B981", "#EAB308"]}

def generate_logo_prompt(brand_name: str, industry: str, style: str) -> str:
    if not groq_client: 
        return f"A modern professional SVG logo concept for '{brand_name}', {industry} industry, minimalist flat vector art, {style}."
        
    prompt = f"Create a highly detailed design brief for an SVG logo. Brand name: '{brand_name}'. Industry: '{industry}'. Design style: '{style}'. Make it optimized for an SVG designer. Include modifiers like clean vector art, flat design, colors. Return ONLY the prompt text."
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=GROQ_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Logo for {brand_name}, {style} style, white background"

def generate_logo(prompt: str, brand_name: str = "Brand", style: str = "Modern"):
    """
    Generates a beautiful local typographic logo using PIL to completely bypass 
    unreliable external APIs and prevent UnidentifiedImageError crashes.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        import math
        
        # 1. Colors based on style
        bg_col = (15, 23, 42) # Slate Dark
        fg_col = (56, 189, 248) # Sky Blue
        
        if "Minimal" in style: bg_col, fg_col = (250, 250, 250), (17, 24, 39)
        elif "Retro" in style: bg_col, fg_col = (244, 235, 219), (217, 119, 67)
        elif "Cyberpunk" in style: bg_col, fg_col = (10, 5, 20), (0, 255, 170)
        elif "Watercolor" in style: bg_col, fg_col = (240, 240, 250), (236, 72, 153)
        elif "3D" in style: bg_col, fg_col = (30, 41, 59), (99, 102, 241)
        
        # 2. Create high-res canvas
        img = Image.new('RGB', (1024, 1024), color=bg_col)
        draw = ImageDraw.Draw(img)
        
        # 3. Draw a modern sleek geometric icon
        cx, cy = 512, 350
        r = 150
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=fg_col, width=24)
        
        # Inner accent
        r2 = 80
        draw.chord([cx-r2, cy-r2, cx+r2, cy+r2], start=0, end=270, fill=fg_col)
        
        # 4. Try loading Arial for crisp typography
        try:
            font_title = ImageFont.truetype("arial.ttf", 120)
            font_sub = ImageFont.truetype("arial.ttf", 50)
        except:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            
        # 5. Draw brand name
        draw.text((512, 650), brand_name.upper(), fill=(255, 255, 255) if sum(bg_col) < 382 else (0, 0, 0), font=font_title, anchor="mm")
        
        # 6. Draw tagline/style
        draw.text((512, 780), f"{style} Concept", fill=fg_col, font=font_sub, anchor="mm")
        
        # 7. Convert to bytes
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()
        
    except Exception as e:
        return f"Local Image Generation Error: {str(e)}"


def chat_with_ai(message: str, history: list) -> str:
    # First try HuggingFace with a strict 10 second timeout
    hf_success = False
    if HF_API_KEY:
        API_URL = f"https://api-inference.huggingface.co/models/{IBM_MODEL}"
        headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Simple history formatting for Granite
        formatted_history = "System: You are a helpful AI branding assistant expert in startups, brand strategy, content marketing, and naming.\n"
        for entry in history[-5:]:  # limit history context
            formatted_history += f"Human: {entry['user']}\nAssistant: {entry['assistant']}\n"
        
        prompt = f"{formatted_history}Human: {message}\nAssistant:"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500, 
                "temperature": 0.5, 
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                    return result[0]['generated_text'].strip()
                return str(result)
            else:
                print(f"HuggingFace API failed with {response.status_code}")
        except Exception as e:
            print(f"HuggingFace API timeout or error: {str(e)}")
            
    # Fallback to Groq if HF is unavailable, acting as IBM Granite
    if groq_client:
        try:
            system_prompt = "You are BizForge's branding strategist. You are powered by IBM Granite (simulated). You are an expert in startups, brand strategy, content marketing, and naming."
            messages = [{"role": "system", "content": system_prompt}]
            
            for entry in history[-5:]:
                messages.append({"role": "user", "content": entry['user']})
                messages.append({"role": "assistant", "content": entry['assistant']})
                
            messages.append({"role": "user", "content": message})
            
            chat_completion = groq_client.chat.completions.create(
                messages=messages,
                model=GROQ_MODEL,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error communicating with fallback AI: {str(e)}"
            
    return "Service unavailable: Both HuggingFace and fallback APIs are disconnected or timing out."

def transcribe_voice(audio_bytes: bytes) -> str:
    if not groq_client: return "Groq API key not configured for transcription."
    try:
        audio_file = ("audio.webm", audio_bytes, "audio/webm")
        translation = groq_client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            response_format="json",
        )
        return translation.text
    except Exception as e:
        return f"Transcription error: {str(e)}"

# Trigger reload
