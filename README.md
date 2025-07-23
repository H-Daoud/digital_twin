# STK Digital Twin Challenge ( Sustainability Case)
# Decision support App 

## Overview
Ein hybrides React + FastAPI System mit LLM + RAG Integration zur Simulation von Produktionskosten, Nachhaltigkeit und politischen Faktoren (CO₂, Zoll, Energie etc.) für mittelständische Industrieunternehmen. Dieses Projekt demonstriert eine Digital-Twin-Simulationsplattform für die STK Produktion GmbH. Sie unterstützt die Simulation von Produktionslogik, Energie-, Kosten- und Nachfrage-Regeln sowie die Analyse auf Basis strukturierter und unstrukturierter (natürlichsprachlicher) Eingaben.

## Features

- **Document upload with OCR and LLM-powered business analysis**
- **Simulation engine with feedback, time steps, and dependency graph**
- **Natural language rule extraction to simulation logic**
- **User-friendly frontend (React/Vite)**

## Stack
- 🔁 Simulation mit Rückkopplung
- 🧠 Azure OpenAI LLM + RAG Chain LangChain Integration
- 📄 OCR für Eingabedokumente (Azure Form Recognizer)
- 📊 BI-Dashboard mit Recharts
- 🧩 Decision Layer zur Unterstützung bei Standortentscheidungen
- 🚀 FastAPI (Python backend)
- 📄 Azure OpenAI & Azure Form Recognizer (LLM + OCR)
- 📦 Vite + React frontend (Frontend, Vite)
- 📄 networkx (Python graph modeling)

## Usage

- Run `pip install -r backend/requirements.txt` and `npm install` in root.
- Start backend: `uvicorn backend.main:app --reload`
- Start frontend: `npm run dev`
- Open `http://localhost:5173`

## Challenge Tasks Addressed

- Simulation model with time, feedback, overrides, and result storage
- Efficient backend logic with caching and API structure
- Natural language to simulation logic with LLMs
- Intuitive UI for business users


## Features
- Upload financial documents for ML-based decisions
- Time-series production cost simulation
- Feedback loops & factory sustainability logic

## Run Locally or via Github codespace with Azure open API + Azure OCR API Keys

### Frontend
```bash
npm install
npm run dev

ASCCII Tree Diagram
│
├── .gitignore
├── LICENSE
├── README.md
├── eslint.config.js
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
│
├── backend/
│   ├── llm_chain.py           # Handles LLM/NLP logic (text→structured info)
│   ├── main.py                # FastAPI backend, API endpoints (simulate, upload)
│   ├── model.py               # Simulation data model & engine (Block, Attribute, SimulationRun)
│   ├── ocr_handler.py         # OCR extraction logic (text from PDF/image)
│   └── requirements.txt       # Python backend dependencies
│
├── public/
│   └── vite.svg               # Static asset(s)
│
└── src/
    ├── App.css
    ├── App.jsx                # Main React frontend
    ├── Upload.jsx             # Upload component
    ├── assets/                # (Images, icons, etc.)
    ├── index.css
    └── main.jsx               # React entry point


🏗️ System Architecture Diagram (Text UML)
 ┌────────────────────┐        HTTP/API        ┌─────────────────────┐
 │   React Frontend   │ <────────────────────> │    FastAPI Backend  │
 └────────────────────┘                        └─────────────────────┘
                                                      │
                                                      │
   ┌──────────────────────────────────────────────────┴──────────────┐
   │                    Backend Modules (Python)                    │
   │                                                                │
   │   ┌────────────┐        ┌───────────────┐         ┌─────────┐  │
   │   │  ocr_handler│        │  llm_chain   │         │  model  │  │
   │   │ (OCR files)│        │(LLM/NLP rules)│        │(simulation│  │
   │   └────────────┘        └───────────────┘         │ engine) │  │
   │                                                   └─────────┘  │
   │  Handles:                                                    │
   │  - Document upload & OCR (extract text)                      │
   │  - LLM for: summary, rule extraction (if needed)             │
   │  - Simulation API (`/simulate/`)                             │
   └──────────────────────────────────────────────────────────────┘
                                                      │
                                                      │
                                   ┌──────────────────┴────────────┐
                                   │         Data Model            │
                                   │ - Block                       │
                                   │ - Attribute                   │
                                   │ - SimulationRun               │
                                   │ - Dependency Graph            │
                                   └───────────────────────────────┘




### References
- [IEEE/ACM, Springer, and referenced scientific works as cited in challenge solution]