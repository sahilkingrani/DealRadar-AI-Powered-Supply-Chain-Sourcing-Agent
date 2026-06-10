# 📡 DealRadar — AI-Powered Supplier Intelligence Agent

> Built for the Bright Data AI Agents & Web Data Hackathon

DealRadar is an intelligent multi-agent system that helps businesses find, 
verify, and analyze suppliers in real-time using Bright Data's web 
infrastructure and Groq AI.

## 🎯 Problem

Finding reliable suppliers takes days of manual research — visiting multiple 
websites, comparing prices, checking reviews, calculating margins. DealRadar 
solves this in under 15 seconds.

## ✨ Features

- 🔍 **Real-time supplier discovery** via Bright Data Web Unlocker
- ✅ **AI-powered verification** with risk scoring (Low/Medium/High)
- 💰 **Profit margin calculation** and ROI projection
- 📡 **Live agent activity feed** showing AI working in real-time
- ⚡ **Results in under 15 seconds**

## 🤖 How It Works — 3 AI Agents

| Agent | Role | Technology |
|-------|------|------------|
| Finder Agent | Discovers suppliers across the web | Bright Data Web Unlocker |
| Verifier Agent | Analyzes quality & assigns risk scores | Groq LLaMA 3.3 70B |
| Margin Agent | Calculates profit potential | Groq LLaMA 3.3 70B |

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **AI:** Groq API (LLaMA 3.3 70B)
- **Web Data:** Bright Data Web Unlocker API
- **Frontend:** React, Vite, Tailwind CSS
- **Architecture:** Multi-agent pipeline

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API key (free at console.groq.com)
- Bright Data API token (free at brightdata.com)

### Installation

**1. Clone the repo:**
```bash
git clone hhttps://github.com/sahilkingrani/DealRadar-AI-Powered-Supply-Chain-Sourcing-Agent
cd dealradar
```

**2. Setup backend:**
```bash
pip install -r requirements.txt
```

**3. Create .env file:**
```env
GROQ_API_KEY=your_groq_key_here
BRIGHTDATA_API_TOKEN=your_brightdata_token_here
APP_HOST=0.0.0.0
APP_PORT=8000
```

**4. Start backend:**
```bash
cd backend
python main.py
```

**5. Setup and start frontend:**
```bash
cd frontend
npm install
npx vite --port 5173
```

**6. Open browser:**

Type any product query like:
- `leather phone cases under $2`
- `wireless earbuds wholesale`
- `custom t-shirts bulk order`

Watch 3 AI agents work in real-time and get verified supplier results!
