from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Dein Bot Token
TOKEN = "8267436644:AAHkIcLdE20tQu7F7FF-mt2PnGjMFVMesGI"

# Texte
WILLKOMMENSTEXT = (
    "Grüß Dich✌️ Du hast eine gute Entscheidung getroffen! "
    "Wir rasieren seit Jahren den Wettmarkt und du kannst jetzt ein Teil davon werden💪 "
    "Bist du ready dafür, mit geilen Wetten mal richtig abzucashen? 😎"
)

JA_TEXT = (
    "Definitiv die richtige Entscheidung💯 Wir liefern dir täglich mehrere Tipps, "
    "hauptsächlich von Fußball und Tennis⚽️🎾. Dabei rasieren wir mit über 80 Prozent Trefferquote "
    "und kassieren richtig ab💰 Für unseren Service und den Aufwand verlangen wir schlappe 30€ im Monat, "
    "also einen Euro am Tag. Das sollte also überhaupt kein Thema sein und falls doch, ist es vermutlich "
    "besser nicht zu wetten, wenn du keine 30€ hast. Zudem hättest du die mit dem ersten Tipp von uns "
    "wieder mehrfach eingespielt😅.\n\n"
    "Wenn du also Bock hast, endlich mit Wetten mal richtig Money zu machen, klicke auf den Link hier "
    "und werde ein Member💪 https://buy.stripe.com/7sY9ATbyNatC93QadY9oc03"
)

NEIN_TEXT = "Schade, aber anscheinend ist nicht jeder dafür gemacht. Trotzdem noch Alles Gute👋"

# Speichert, welche User schon begrüßt wurden
begruesste_user = set()

# Willkommensnachricht mit Buttons
async def send_welcome_message(chat_id, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Ja Safe🔥", callback_data="ja"),
            InlineKeyboardButton("Nein🔴", callback_data="nein"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=WILLKOMMENSTEXT, reply_markup=reply_markup)

# Start-Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in begruesste_user:
        begruesste_user.add(user_id)
        await send_welcome_message(update.effective_chat.id, context)

# Jede erste Nachricht eines Users
async def first_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in begruesste_user:
        begruesste_user.add(user_id)
        await send_welcome_message(update.effective_chat.id, context)

# Button-Antworten
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Bestätigung für Telegram

    if query.data == "ja":
        await query.edit_message_text(JA_TEXT)
    elif query.data == "nein":
        await query.edit_message_text(NEIN_TEXT)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, first_message))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()
