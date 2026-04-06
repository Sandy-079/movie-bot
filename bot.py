import json
import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

ADMIN_ID = 1109352172  # mee Telegram ID

# Load movies
def load_movies():
    with open("movies.json") as f:
        return json.load(f)

def save_movies(data):
    with open("movies.json", "w") as f:
        json.dump(data, f, indent=4)

# Start command (buttons)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movies = load_movies()

    keyboard = []
    for key, movie in movies.items():
        keyboard.append([InlineKeyboardButton(movie["title"], callback_data=key)])

    await update.message.reply_text(
        "🎬 Choose movie:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Button click
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    movies = load_movies()
    movie_id = query.data

    if movie_id in movies:
        movie = movies[movie_id]
        await query.message.reply_video(
            video=movie["file"],
            caption=f"🎬 {movie['title']}"
        )

# Add movie
async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Not admin")
        return

    try:
        movie_id = context.args[0]
        title = context.args[1]
        link = context.args[2]

        movies = load_movies()
        movies[movie_id] = {"title": title, "file": link}
        save_movies(movies)

        await update.message.reply_text("✅ Movie added")
    except:
        await update.message.reply_text("Usage:\n/add id title link")

# List movies
async def list_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movies = load_movies()
    text = "\n".join([f"{k} - {v['title']}" for k, v in movies.items()])
    await update.message.reply_text(text or "No movies")

# RUN BOT (IMPORTANT FIX)
app = ApplicationBuilder().token(config.TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_movie))
app.add_handler(CommandHandler("list", list_movies))
app.add_handler(CallbackQueryHandler(button))

print("Bot running 🚀")
app.run_polling()
