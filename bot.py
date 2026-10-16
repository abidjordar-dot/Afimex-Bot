import os
import logging
from asyncio import ThreadSafeLoop
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# 1. Fake Web Server for Render Health Check
app = Flask(__name__)

@app.route('/')
def home():
    return "Afimex Bot is Alive & Running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram Bot Configuration
TOKEN = "8817520853:AAGXapOzgjkK0iOA1iKG7k_TjKy3aBpEBB8"
MAIN_CHANNEL = "@Afimex001"
PAYMENT_CHANNEL = "@Afimexpayment"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_joined(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=MAIN_CHANNEL, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    
    is_joined = await check_joined(user_id, context)
    
    if not is_joined:
        keyboard = [
            [InlineKeyboardButton("📢 Main Channel Join", url="https://t.me/Afimex001")],
            [InlineKeyboardButton("💳 Payment Proof Channel", url="https://t.me/Afimexpayment")],
            [InlineKeyboardButton("✅ Checked / Verified", callback_data="check_join")]
        ]
        welcome_text = (
            f"👋 আসসালামু আলাইকুম {first_name}!\n\n"
            f"🔥 **Afimex**-এ আপনাকে স্বাগতম!\n"
            f"অনলাইন থেকে ঘরে বসেই প্রতিদিন ২০০-৩০০ টাকা আয় করার সেরা প্ল্যাটফর্ম।\n\n"
            f"⚠️ **শর্তাবলী:** বটে কাজ শুরু করতে প্রথমে আমাদের ২টি চ্যানেলে বাধ্যতামূলক জয়েন হতে হবে।"
        )
        await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await send_main_menu(update, context)

async def send_main_menu(update, context):
    menu_buttons = [
        ['💰 অ্যাড দেখুন', '👥 রেফার করুন'],
        ['🔓 আইডি অ্যাক্টিভ করুন', '💳 উইথড্র'],
        ['📊 মাই প্রোফাইল', '📞 সাপোর্ট']
    ]
    msg_text = (
        "🎉 **অভিনন্দন! আপনার অ্যাকাউন্ট সফলভাবে ভেরিফাই হয়েছে।**\n\n"
        "নিচের মেনু থেকে আপনার কাঙ্ক্ষিত অপশনটি বেছে নিন এবং কাজ শুরু করুন!"
    )
    markup = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True)
    if update.message:
        await update.message.reply_text(msg_text, reply_markup=markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg_text, reply_markup=markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "check_join":
        if await check_joined(query.from_user.id, context):
            await query.message.delete()
            await send_main_menu(update, context)
        else:
            await query.message.reply_text("❌ আপনি এখনো আমাদের চ্যানেলে জয়েন করেননি! দয়া করে জয়েন করে 'Checked' বাটনে চাপুন।")

if __name__ == '__main__':
    # Start Web Server in a Background Thread
    server_thread = Thread(target=run_flask)
    server_thread.start()
    
    # Start Telegram Bot
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler('start', start))
    bot_app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Afimex Bot & Server are Running...")
    bot_app.run_polling()
