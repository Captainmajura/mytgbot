from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Payment and Account Details
ACCOUNT_NAME = "James Fredrick Majura"
ACCOUNT_NUMBER = "51710065661"
PAYMENT_AMOUNT = "15,000 TZS"

# Function to start the bot and send a welcome message
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    language_button = [[KeyboardButton("English"), KeyboardButton("Swahili")]]
    reply_markup = ReplyKeyboardMarkup(language_button, one_time_keyboard=True)

    await update.message.reply_text(
        f"Hi {user.first_name}, welcome to Predictor Aviator!",
        reply_markup=reply_markup
    )
    await update.message.reply_text("Please choose your language:")

# Function to handle the language selection
async def language_selection(update: Update, context: CallbackContext) -> None:
    selected_language = update.message.text.lower()

    if selected_language == "english":
        context.user_data['language'] = 'english'
        await send_payment_info(update, context)
    elif selected_language == "swahili":
        context.user_data['language'] = 'swahili'
        await send_payment_info(update, context)
    else:
        await update.message.reply_text("Please choose a valid language option.")

# Function to send payment info
async def send_payment_info(update: Update, context: CallbackContext) -> None:
    language = context.user_data.get('language', 'english')

    if language == "english":
        await update.message.reply_text(
            f"To create your account, please pay {PAYMENT_AMOUNT}.")
        await update.message.reply_text(
            f"Pay us via NMB\nName: {ACCOUNT_NAME}\nACC NO: {ACCOUNT_NUMBER}")
        await update.message.reply_text(
            "Once you've made the payment, please send the proof here, and we'll verify it.")
    elif language == "swahili":
        await update.message.reply_text(
            f"Ili kuunda akaunti yako, tafadhali lipa {PAYMENT_AMOUNT}.")
        await update.message.reply_text(
            f"Lipa kupitia NMB\nJina: {ACCOUNT_NAME}\nACC NO: {ACCOUNT_NUMBER}")
        await update.message.reply_text(
            "Baada ya kufanya malipo, tafadhali tuma uthibitisho hapa, na tutakuthibitisha.")

# Function to handle payment confirmation
async def handle_proof_of_payment(update: Update, context: CallbackContext) -> None:
    language = context.user_data.get('language', 'english')

    if language == "english":
        await update.message.reply_text("Thank you! We will verify your payment shortly.")
    elif language == "swahili":
        await update.message.reply_text("Asante! Tutathibitisha malipo yako hivi karibuni.")

# Main function to run the bot
async def main():
    application = ApplicationBuilder().token(os.getenv("7260094906:AAHiJQ3laBzGfGrUUZ1ATnutTi1tRuFP3Io")).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))

    # Message Handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, language_selection))
    application.add_handler(MessageHandler(filters.PHOTO | filters.TEXT & filters.Command, handle_proof_of_payment))

    # Run the bot
    await application.run_polling()

# Run the bot if this script is executed
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
