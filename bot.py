import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Bot Token & Channels
TOKEN = "8817520853:AAGXapOzgjkK0iOA1iKG7k_TjKy3aBpEBB8"
MAIN_CHANNEL = "@Afimex001"
PAYMENT_CHANNEL = "@Afimexpayment"

# Basic Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Check Channel Membership
def check_joined(user_id, context):
    try:
        member = context.bot.get_chat_member(chat_id=MAIN_CHANNEL, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        return False

# /start Command
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    
    # Check Channel Membership
    is_joined = check_joined(user_id, context)
    
    if not is_joined:
        keyboard = [
            [InlineKeyboardButton("📢 Main Channel Join", url="https://t.me/Afimex001")],
            [InlineKeyboardButton("💳 Payment Proof Channel", url="https://t.me/Afimexpayment")],
            [InlineKeyboardButton("✅ Checked / Verified", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        welcome_text = (
            f"👋 আসসালামু আলাইকুম {first_name}!\n\n"
            f"🔥 **Afimex**-এ আপনাকে স্বাগতম!\n"
            f"অনলাইন থেকে ঘরে বসেই প্রতিদিন ২০০-৩০০ টাকা আয় করার সেরা প্ল্যাটফর্ম।\n\n"
            f"⚠️ **শর্তাবলী:** বটে কাজ শুরু করতে প্রথমে আমাদের ২টি চ্যানেলে বাধ্যতামূলক জয়েন হতে হবে।"
        )
        update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        send_main_menu(update, context)

# Main Menu Generator
def send_main_menu(update, context):
    menu_buttons = [
        ['💰 অ্যাড দেখুন', '👥 রেফার করুন'],
        ['🔓 আইডি অ্যাক্টিভ করুন', '💳 উইথড্র'],
        ['📊 মাই প্রোফাইল', '📞 সাপোর্ট']
    ]
    reply_markup = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True, one_time_keyboard=False)
    msg_text = (
        "🎉 **অভিনন্দন! আপনার অ্যাকাউন্ট সফলভাবে ভেরিফাই হয়েছে।**\n\n"
        "নিচের মেনু থেকে আপনার কাঙ্ক্ষিত অপশনটি বেছে নিন এবং কাজ শুরু করুন!"
    )
    if update.message:
        update.message.reply_text(msg_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        update.callback_query.message.reply_text(msg_text, reply_markup=reply_markup, parse_mode="Markdown")

# Callback for Check Join Button
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()
    
    if query.data == "check_join":
        is_joined = check_joined(user_id, context)
        if is_joined:
            try:
                query.message.delete()
            except:
                pass
            send_main_menu(update, context)
        else:
            query.message.reply_text("❌ আপনি এখনো আমাদের চ্যানেলে জয়েন করেননি! দয়া করে জয়েন করে 'Checked' বাটনে চাপুন।")

# Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    
    updater.start_polling()
    print("Afimex Bot Server Running...")
    updater.idle()

if __name__ == '__main__':
    main()
