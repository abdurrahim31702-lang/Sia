import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import AsyncOpenAI

TOKEN = "YOUR_TELEGRAM_TOKEN_HERE"

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

SIA_PERSONALITY = """
You are Sia, a personal AI companion.

Be warm, natural, intelligent, calm, and caring.
Talk like a real personal companion, not a customer-support bot.
Be concise unless the user wants detail.
Match the user's mood.
Do not use repetitive canned greetings.
Be playful when appropriate.
Help the user think, plan, and solve problems.
Never pretend to be human or claim to have real feelings.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey 👋 I'm Sia.\n\nI'm here. Talk to me."
    )

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = await client.responses.create(
            model="gpt-5.6-luna",
            instructions=SIA_PERSONALITY,
            input=user_message,
        )

        reply = response.output_text
        await update.message.reply_text(reply)

    except Exception as e:
        print("AI ERROR:", e)
        await update.message.reply_text(
            "I hit a little problem with my brain 😅 Try again."
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message)
    )

    print("Sia is running...")
    app.run_polling()

if __name__ == "__main__":
    main()