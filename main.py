import os
from fastapi import FastAPI, Request, Form
from anthropic import Anthropic
from twilio.rest import Client

app = FastAPI()
claude = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
twilio = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

conversations = {}

@app.post("/webhook")
async def webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    user_number = From
    user_text = Body

    if user_number not in conversations:
        conversations[user_number] = []
    conversations[user_number].append({"role": "user", "content": user_text})

    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system="أنت مساعد ذكي ودود. رد دائماً بالعربية ما لم يتحدث المستخدم بلغة أخرى.",
        messages=conversations[user_number]
    )
    reply = response.content[0].text

    conversations[user_number].append({"role": "assistant", "content": reply})

    twilio.messages.create(
        from_="whatsapp:+14155238886",
        to=user_number,
        body=reply
    )

    return {"status": "ok"}
