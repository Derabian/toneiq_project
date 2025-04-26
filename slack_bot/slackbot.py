
import os, base64, requests
from slack_bolt import App
from dotenv import load_dotenv

load_dotenv()
app = App(token=os.getenv("SLACK_BOT_TOKEN"), signing_secret=os.getenv("SLACK_SIGNING_SECRET"))
BACKEND = os.getenv("BACKEND_URL","http://localhost:8000")

@app.command('/toneiq')
def handle_cmd(ack, body, respond, files=None):
    ack()
    text = body.get('text') or ''
    respond('🎤 Upload an audio file in this thread and mention me to analyze.')

@app.event('message')
def handle_message(event, say):
    if 'files' in event and '<@' in event['text']:
        file_info = event['files'][0]
        url = file_info['url_private']
        headers={'Authorization':f"Bearer {os.getenv('SLACK_BOT_TOKEN')}"}
        audio = requests.get(url,headers=headers).content
        audio_b64 = base64.b64encode(audio).decode()
        payload={'audio':audio_b64,'message':event['text']}
        res = requests.post(f"{BACKEND}/analyze", json=payload).json()
        say(res['revised_message'])
        say(res['audio_base64'])

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
