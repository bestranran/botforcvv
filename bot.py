from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN
from database import init_db
from handlers import start, button_handler, deposit_handler, add_product

def main():
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), deposit_handler))
    app.add_handler(CommandHandler("add_product", add_product))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
