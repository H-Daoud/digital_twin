import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from ocr_handler import extract_text_from_file
from llm_chain import ask_llm

# 🔐 .env Variablen laden
load_dotenv()


FORM_ENDPOINT = os.getenv("form_endpoint")
FORM_KEY = os.getenv("form_key")
API_KEY = os.getenv("AZURE_API_KEY")
ENDPOINT = os.getenv("AZURE_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION")

# 🚀 FastAPI App starten
app = FastAPI()

# 🌍 CORS erlauben (z. B. für React Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion: domains explizit setzen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔎 Health Check
@app.get("/")
def root():
    return {"message": "🚀 STK Digital Twin – Backend API läuft!"}

# 📤 Upload & Analyse Endpoint
@app.post("/analyze-upload/")
async def analyze_document(file: UploadFile = File(...)):
    try:
        text = await extract_text_from_file(file)         # ⬅ OCR (Form Recognizer)
        llm_response = ask_llm(text)                      # ⬅ Azure OpenAI GPT-4o
        return {
            "filename": file.filename,
            "extracted_text": text,
            "llm_interpretation": llm_response
        }
    except Exception as e:
        return {
            "error": str(e)
        }
