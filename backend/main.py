import os
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.ocr_handler import extract_text_from_file
from backend.llm_chain import ask_llm, extract_structured_logic
from backend.model import Attribute, Block, SimulationRun
import json
import hashlib

# Load .env variables
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic health check
@app.get("/")
def root():
    return {"message": "🚀 STK Digital Twin – Backend API running!"}

# OCR + LLM summary endpoint
@app.post("/analyze-upload/")
async def analyze_document(file: UploadFile = File(...)):
    try:
        text = await extract_text_from_file(file)
        llm_response = ask_llm(text)
        return {"text": text, "llm_analysis": llm_response}
    except Exception as e:
        return {"error": str(e)}

# Rule extraction endpoint (Task 3)
@app.post("/extract-rule/")
async def extract_rule(request: Request):
    body = await request.json()
    rule_text = body.get("rule", "")
    structured_rule = extract_structured_logic(rule_text)
    return {"rule": rule_text, "structured": structured_rule}

# --- Simulation logic ---

def hash_config(config: dict) -> str:
    config_str = json.dumps(config, sort_keys=True)
    return hashlib.sha256(config_str.encode()).hexdigest()

cache_store = {}

@app.post("/simulate/")
async def simulate(request: Request):
    payload = await request.json()
    steps = payload.get("steps", 10)
    raw_blocks = payload.get("blocks", {})

    blocks = {}
    for block_name, attrs in raw_blocks.items():
        attr_objs = {}
        for attr_name, attr_data in attrs.items():
            is_input = attr_data.get("is_input", True)
            value = attr_data.get("value", None)
            dependencies = attr_data.get("dependencies", [])
            attr_objs[attr_name] = Attribute(
                name=attr_name,
                is_input=is_input,
                value=value,
                dependencies=dependencies,
                formula=None  # Extend for formula support
            )
        blocks[block_name] = Block(name=block_name, attributes=attr_objs)

    sim = SimulationRun(name="default_sim", steps=steps, blocks=blocks)
    sim.run()
    return {"results": sim.results}

# Cached simulation endpoint
@app.post("/simulate_cached/")
async def simulate_cached(request: Request):
    payload = await request.json()
    cache_key = hash_config(payload)
    if cache_key in cache_store:
        return {"cached": True, "results": cache_store[cache_key]}
    # Otherwise run and store
    steps = payload.get("steps", 10)
    raw_blocks = payload.get("blocks", {})

    blocks = {}
    for block_name, attrs in raw_blocks.items():
        attr_objs = {}
        for attr_name, attr_data in attrs.items():
            is_input = attr_data.get("is_input", True)
            value = attr_data.get("value", None)
            dependencies = attr_data.get("dependencies", [])
            attr_objs[attr_name] = Attribute(
                name=attr_name,
                is_input=is_input,
                value=value,
                dependencies=dependencies,
                formula=None
            )
        blocks[block_name] = Block(name=block_name, attributes=attr_objs)

    sim = SimulationRun(name="cached_sim", steps=steps, blocks=blocks)
    sim.run()
    cache_store[cache_key] = sim.results
    return {"cached": False, "results": sim.results}
