# Digital Twin Decision Support App

Ein hybrides React + FastAPI System mit LLM + RAG Integration zur Simulation von Produktionskosten, Nachhaltigkeit und politischen Faktoren (CO₂, Zoll, Energie etc.) für mittelständische Industrieunternehmen.

## Features
- 🔁 Simulation mit Rückkopplung
- 🧠 LLM + LangChain Integration
- 📄 OCR für Eingabedokumente (Azure Form Recognizer)
- 📊 BI-Dashboard mit Recharts
- 🧩 Decision Layer zur Unterstützung bei Standortentscheidungen
# STK Digital Twin (VW Sustainability Case)

This app simulates and evaluates factory operations using:
- 🧠 Azure OpenAI LLM + RAG Chain
- 🧾 Azure Form Recognizer OCR for financial uploads
- 📊 Recharts visualization
- 📦 Vite + React frontend
- 🚀 FastAPI backend

## Features
- Upload financial documents for ML-based decisions
- Time-series production cost simulation
- Feedback loops & factory sustainability logic

## Run Locally

### Frontend
```bash
npm install
npm run dev

## Struktur
- `src/`: Frontend (React + Vite)
- `backend/`: API + LLM + OCR
digital_twin/
├── .gitignore
├── README.md
├── LICENSE
├── package.json
├── vite.config.js
├── src/               ← React frontend
├── backend/           ← Python FastAPI backend
│   ├── main.py
│   ├── ocr_handler.py
│   ├── llm_chain.py
│   ├── requirements.txt
│   └── .env           ✅ HERE — for API keys & backend config
└── .env (optional)    ⛔️ Only if frontend uses env vars (not common)

