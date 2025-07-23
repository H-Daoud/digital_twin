import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from ocr_handler import extract_text_from_file
from llm_chain import ask_llm


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🔐 .env Variablen laden
load_dotenv()

import os

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION")

FORM_ENDPOINT = os.getenv("FORM_ENDPOINT")
FORM_KEY = os.getenv("FORM_KEY")

OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
MODEL_NAME = os.getenv("MODEL_NAME")
OPENAI_VERSION = os.getenv("OPENAI_VERSION")



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
