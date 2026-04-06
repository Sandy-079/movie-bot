import json
import config
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load movies
with open("movies.json") as f:
    movies = json.load(f)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        movie_id = context.args[0]

        if movie_id in movies:
            await update.message.reply_video(
                video=movies[movie_id]["file"],
                caption=movies[movie_id]["title"]
            )
        else:
            await update.message.reply_text("❌ Movie not found")
    else:
        await update.message.reply_text("👋 Welcome")

# ✅ SAFE RUN (Render compatible)
async def main():
    app = ApplicationBuilder().token(config.TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot started...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
