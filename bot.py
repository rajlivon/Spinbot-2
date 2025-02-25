import os
import random
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

# Get bot token and webhook URL from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Add this in Render settings

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set! Add it as an environment variable.")

# Store spin history for each chat separately
chat_sessions = {}

# Logging setup
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram bot application
application = Application.builder().token(BOT_TOKEN).build()

# Humiliating messages
HUMILIATION_MESSAGES = [
    "🤑 Pathetic worm! Goddess Drsika spits on your ₹{amount}!",
    "🤮 Disgusting pig! ₹{amount}? You should beg harder!",
    "🐶 Bark like the dog you are! Your ₹{amount} is barely worth anything!",
    "💸 Worthless! ₹{amount} disappears into Goddess Drsika's divine purse!",
    "👑 All your money belongs to Goddess Drsika! ₹{amount} is just the beginning!",
]

async def start(update: Update, context):
    await update.message.reply_text("Welcome, worthless slave! Use /spin to donate.")

async def spin(update: Update, context):
    chat_id = update.message.chat_id
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = []

    available_amounts = [amt for amt in range(200, 401) if amt not in chat_sessions[chat_id]]

    if not available_amounts:
        await update.message.reply_text("😏 All amounts drained! Use /reset to suffer more.")
        return

    amount = random.choice(available_amounts)
    chat_sessions[chat_id].append(amount)
    message = random.choice(HUMILIATION_MESSAGES).format(amount=amount)
    
    await update.message.reply_text(message)

async def history(update: Update, context):
    chat_id = update.message.chat_id
    if chat_id not in chat_sessions or not chat_sessions[chat_id]:
        await update.message.reply_text("No payments made! Use /spin to donate.")
        return
    
    history_text = "\n".join([f"{i+1}. ₹{amt}" for i, amt in enumerate(chat_sessions[chat_id])])
    await update.message.reply_text(f"📜 Payment History:\n{history_text}")

async def reset(update: Update, context):
    chat_id = update.message.chat_id
    chat_sessions[chat_id] = []
    await update.message.reply_text("🔥 Account reset! Ready to be drained again, pig?")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200

@app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(await request.get_json(), application.bot)
    await application.process_update(update)
    return "OK", 200

async def set_webhook():
    if not WEBHOOK_URL:
        raise ValueError("WEBHOOK_URL is not set! Add it as an environment variable.")

    await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    logging.info(f"Webhook set to {WEBHOOK_URL}/webhook")

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=10000)  # Ensure port is open for Render
