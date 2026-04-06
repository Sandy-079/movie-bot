import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import config

with open("movies.json") as f:
    movies = json.load(f)

async def is_user_joined(bot, user_id):
    try:
        member = await bot.get_chat_member(config.CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_user_joined(context.bot, user_id):
        await update.message.reply_text(f"Join channel: {config.CHANNEL_USERNAME}")
        return

    if context.args:
        movie_id = context.args[0]
        if movie_id in movies:
            await update.message.reply_video(
                video=movies[movie_id]["file"],
                caption=movies[movie_id]["title"]
            )
        else:
            await update.message.reply_text("Not found ❌")
    else:
        await update.message.reply_text("Welcome 👋")

app = ApplicationBuilder().token(config.TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()