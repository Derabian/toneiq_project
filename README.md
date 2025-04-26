# Tone‑IQ – Cross‑Channel Tone‑to‑Intent Translator

A demo package that shows how to:
* detect emotional tone from audio
* rewrite intent with GPT‑4
* auto‑create well‑being‑aware Cases in Salesforce
* suggest empathy macros
* respond in Slack with rewritten text + synthesized voice

## Folders
```
backend/      FastAPI server (tone analysis + GPT + ElevenLabs)
salesforce/   Lightning Web Component + Apex controller
slack_bot/    Slack Bolt bot that calls the same FastAPI
```

## Quick Start
### 1. Backend (local)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your keys
uvicorn app:app --reload
```

### 2. Salesforce
* Authenticate with Salesforce CLI  
* `sfdx force:project:create -n toneiq` (or reuse this folder)  
* Copy `salesforce/` into `force-app/main/default/`  
* `sfdx force:source:deploy -p force-app`  

### 3. Slack Bot
```bash
cd slack_bot
pip install -r requirements.txt
export SLACK_BOT_TOKEN=xxx SLACK_SIGNING_SECRET=yyy BACKEND_URL=http://localhost:8000
python slackbot.py
```

Detailed instructions are inside each sub‑folder.
