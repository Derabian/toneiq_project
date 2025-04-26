
import os, base64, tempfile, librosa, numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
from elevenlabs import generate, save, set_api_key

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

app = FastAPI()

class AnalyzeRequest(BaseModel):
    audio: str  # base64 wav/mp3
    message: str | None = ""

@app.get("/health")
def health():
    return {"status": "ok"}

def describe_audio(path):
    y, sr = librosa.load(path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    pitch = librosa.yin(y, fmin=50, fmax=300, sr=sr)
    intensity = float(np.mean(librosa.feature.rms(y=y)))
    tone = "frustrated" if intensity > 0.04 else "calm"
    intent = "Burnout_Risk" if tone == "frustrated" else "Neutral"
    stress = round(min(intensity * 30, 1.0), 2)
    description = f"Duration {duration:.1f}s, pitch {int(pitch.min())}-{int(pitch.max())}Hz, intensity {intensity:.4f}"
    return description, tone, intent, stress

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        wav_bytes = base64.b64decode(req.audio)
    except Exception:
        raise HTTPException(400, "invalid base64")

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp.write(wav_bytes)
        tmp_path = tmp.name

    desc, tone, intent, stress = describe_audio(tmp_path)

    prompt_system = "Rewrite the message to match the emotional tone."
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":prompt_system},
            {"role":"user","content":f"Message: '{req.message}' Tone: {tone}"}
        ]
    )
    revised = completion.choices[0].message.content.strip()

    audio_bytes = generate(text=revised, voice="Rachel", model="eleven_multilingual_v2")
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as out:
        save(audio_bytes, out.name)
        mp3_b64 = base64.b64encode(open(out.name,'rb').read()).decode()

    return {
        "revised_message": revised,
        "audio_base64": mp3_b64,
        "tone": tone,
        "intent": intent,
        "stress_score": stress
    }
