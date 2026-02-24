from fastapi import FastAPI, Request
import stripe
import os
from core.database.connection import get_db

app = FastAPI()

stripe.api_key = os.getenv("STRIPE_SECRET")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return {"error": str(e)}

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = session["metadata"]["user_id"]
        amount = session["amount_total"] / 100

        db = get_db()
        db.users.update_one(
            {"telegram_id": int(user_id)},
            {"$inc": {"balance": amount}}
        )

    return {"status": "success"}
