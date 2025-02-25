import os
import random
import logging
import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler

# Load bot token and webhook URL from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set this in Render settings
PORT = int(os.getenv("PORT", 10000))  # Default port for Flask

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

# --- Telegram Bot Handlers ---

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

# --- Flask Routes ---

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Bot is running!"})

@app.route("/webhook", methods=["POST"])
async def webhook():
    """Process incoming webhook updates from Telegram."""
    try:
        update = Update.de_json(request.get_json(), application.bot)
        await application.process_update(update)
    except Exception as e:
        logging.error(f"Error processing update: {e}")
    return jsonify({"status": "ok"}), 200

# --- Webhook Setup ---

async def set_webhook():
    if not WEBHOOK_URL:
        logging.error("WEBHOOK_URL is missing! Please set it in Render settings.")
        return
    
    try:
        success = await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
        if success:
            logging.info(f"✅ Webhook successfully set to {WEBHOOK_URL}/webhook")
        else:
            logging.error("❌ Failed to set webhook! Check your bot token & URL.")
    except Exception as e:
        logging.error(f"⚠️ Error setting webhook: {e}")

# --- Running the Bot and Flask ---

async def main():
    """Start the Telegram bot and Flask web server."""
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("spin", spin))
    application.add_handler(CommandHandler("history", history))
    application.add_handler(CommandHandler("reset", reset))

    # Set webhook for Telegram bot
    await set_webhook()

    # Run Flask in an async-friendly way
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = [f"0.0.0.0:{PORT}"]
    await serve(app, config)

if __name__ == "__main__":
    # Run everything inside asyncio event loop
    asyncio.run(main())
