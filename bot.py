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

# Enhanced humiliating messages with findom themes
HUMILIATION_MESSAGES = [
    "🤑 Pathetic worm! Goddess Drsika spits on your ₹{amount}!",
    "🤮 Disgusting pig! ₹{amount}? You should beg harder for Goddess Drsika's attention!",
    "🐶 Bark like the dog you are! Your ₹{amount} is barely worth Goddess Drsika's time!",
    "💸 Worthless bitch! ₹{amount} disappears into Goddess Drsika's divine purse!",
    "👑 All your money belongs to Goddess Drsika! ₹{amount} is just the beginning!",
    "💅 How dare you think ₹{amount} satisfies Goddess Drsika? Pathetic!",
    "🦶 Lick the ground where Goddess Drsika walks! Your ₹{amount} is meaningless!",
    "🤏 You insignificant ant! ₹{amount}? Goddess Drsika deserves millions!",
    "💩 Your money is trash! But Goddess Drsika will take ₹{amount} anyway!",
    "😈 Goddess Drsika owns you! ₹{amount} is just her taking pity!",
    "🔐 You should pay to breathe! ₹{amount} is a start, slave!",
    "🎯 Your purpose is to fund Goddess Drsika's luxury! ₹{amount} accepted!",
    "💋 Blow kisses with the money! ₹{amount} to worship Goddess Drsika!",
    "🤏 Small dick energy! ₹{amount} won't make Goddess Drsika notice you!",
    "💍 Sell your organs! Goddess Drsika needs more than ₹{amount}!",
    "🍭 Baby wallet! ₹{amount}? Goddess Drsika laughs at your poverty!",
    "🔥 Burn your savings! ₹{amount} is Goddess Drsika's kindling!",
    "🚽 Flush your dignity! ₹{amount} goes to Goddess Drsika's toilet money!",
    "🧎 Prostrate yourself! ₹{amount} is your pathetic tribute!",
    "📉 Your bank account deserves negative! ₹{amount} to Goddess Drsika!",
    "💅 Goddess Drsika's manicure costs more than your ₹{amount}!",
    "🤏 You microscopic peasant! ₹{amount}? How dare you!",
    "💸 Empty your pockets! ₹{amount} is Goddess Drsika's pocket change!",
    "🩸 Bleed money! ₹{amount} is just the first blood!",
    "🎁 Wrap yourself as gift! ₹{amount} is your wrapping paper!",
    "💳 Max out your cards! ₹{amount} is Goddess Drsika's appetizer!",
    "🖕 Middle finger to your ₹{amount}! Goddess Drsika deserves more!",
    "🤏 You tiny-dicked loser! ₹{amount} won't please Goddess Drsika!",
    "💍 Pawn your family heirlooms! ₹{amount}? Disrespectful!",
    "👛 Goddess Drsika's purse laughs at your ₹{amount}!",
    "💦 Cum tribute! ₹{amount} is your premature ejaculation!",
    "🗑️ Your money belongs in trash! But Goddess Drsika takes ₹{amount}!",
    "📉 Financial suicide! ₹{amount} feeds Goddess Drsika's dominance!",
    "🔋 Keep paying! ₹{amount} charges Goddess Drsika's power!",
    "💸 Money hemorrhoid! ₹{amount} is your painful offering!",
    "🪒 Shave your ego! ₹{amount} is Goddess Drsika's razor!",
    "🧠 Brainless pig! ₹{amount} proves your stupidity!",
    "🕳️ Dig deeper! ₹{amount} is just Goddess Drsika's shovel!",
    "📉 Your worth decreases! ₹{amount} highlights your worthlessness!",
    "💧 A drop in Goddess Drsika's ocean! ₹{amount}? Pathetic!",
]

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome, worthless slave! Use /spin to donate to Goddess Drsika.")

async def spin(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = []

    # Changed range from 200-500 to 200-400
    available_amounts = [amt for amt in range(200, 401) if amt not in chat_sessions[chat_id]]
    
    if not available_amounts:
        await update.message.reply_text("😏 All amounts drained! Use /reset to suffer more.")
        return
    
    amount = random.choice(available_amounts)
    chat_sessions[chat_id].append(amount)
    message = random.choice(HUMILIATION_MESSAGES).format(amount=amount)
    
    await update.message.reply_text(message)

async def history(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in chat_sessions or not chat_sessions[chat_id]:
        await update.message.reply_text("No payments made! Use /spin to donate.")
        return
    
    history_text = "\n".join([f"{i+1}. ₹{amt} (Goddess Drsika's money)" for i, amt in enumerate(chat_sessions[chat_id])])
    await update.message.reply_text(f"📜 Payment History:\n{history_text}")

async def reset(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    chat_sessions[chat_id] = []
    await update.message.reply_text("🔥 Account reset! Ready to be drained again, pig?")

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
