import logging
import random
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set! Add it as an environment variable.")

# Store spin history for each chat separately
chat_sessions = {}

# Logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Humiliating messages for spin
HUMILIATION_MESSAGES = [
    "😂 Look at you, a broke little servant of Goddess Smriti! You only got ₹{amount}.",
    "🤡 Goddess Smriti laughs at your misery! ₹{amount} is all you get, loser!",
    "🤣 You think you deserve more? Goddess Smriti says take your ₹{amount} and cry!",
    "😆 Pathetic! Goddess Smriti owns you, and ₹{amount} is all you shall have!",
    "🙃 Even ₹{amount} is too much for a lowly worm like you! Bow to Goddess Smriti!",
]

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome, servant! Use /spin to spin the wheel.")

async def spin(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = []

    available_amounts = [amt for amt in range(200, 501) if amt not in chat_sessions[chat_id]]
    
    if not available_amounts:
        await update.message.reply_text("😏 All amounts have been used! Use /reset.")
        return
    
    amount = random.choice(available_amounts)
    chat_sessions[chat_id].append(amount)
    message = random.choice(HUMILIATION_MESSAGES).format(amount=amount)
    
    await update.message.reply_text(message)

async def history(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in chat_sessions or not chat_sessions[chat_id]:
        await update.message.reply_text("No spins yet! Use /spin.")
        return
    
    history_text = "\n".join([f"{i+1}. ₹{amt}" for i, amt in enumerate(chat_sessions[chat_id])])
    await update.message.reply_text(f"📜 Spin History:\n{history_text}")

async def reset(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    chat_sessions[chat_id] = []
    await update.message.reply_text("🔄 Reset complete!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spin", spin))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("reset", reset))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
