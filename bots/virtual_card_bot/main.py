import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ================= MAIN MENU ================= #

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Buy Cards", callback_data="buy")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("📦 My Orders", callback_data="orders")],
        [InlineKeyboardButton("📊 Balance", callback_data="balance")],
        [InlineKeyboardButton("🆘 Support", callback_data="support")]
    ])

# ================= BUY MENU ================= #

def buy_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇸 Visa USA", callback_data="visa_usa"),
         InlineKeyboardButton("🇨🇦 Visa Canada", callback_data="visa_ca")],
        [InlineKeyboardButton("💳 MasterCard USA", callback_data="mc_usa"),
         InlineKeyboardButton("💳 MasterCard Canada", callback_data="mc_ca")],
        [InlineKeyboardButton("⚙ Filter", callback_data="filter")],
        [InlineKeyboardButton("🔙 Back", callback_data="main")]
    ])

# ================= FILTER MENU ================= #

def filter_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("≤ $10", callback_data="f10"),
         InlineKeyboardButton("≤ $50", callback_data="f50")],
        [InlineKeyboardButton("> $50", callback_data="f50plus")],
        [InlineKeyboardButton("🔙 Back", callback_data="buy")]
    ])

# ================= DEPOSIT MENU ================= #

def deposit_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Pay with Card", url="https://your-stripe-link.com")],
        [InlineKeyboardButton("📲 QR Payment", callback_data="qr")],
        [InlineKeyboardButton("🔙 Back", callback_data="main")]
    ])

# ================= START ================= #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """★彡━━━━━━━━━━━━彡★
   ╔═══════🅖Ⓤ🅡Ⓥ═══════╗
𝔊✦𝔙                     𝓖ΞΞΞΞΞΞ   𝓖𝓤𝓡𝓤⦿\/𝓐𝓘
   ╚═══════🅖Ⓤ🅡Ⓥ═══════╝
★彡━━━━━━━━━━━━彡★

💎 Premium Card Marketplace
""",
        reply_markup=main_menu()
    )

# ================= CALLBACK HANDLER ================= #

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        await query.edit_message_text("💳 Select Card Type:", reply_markup=buy_menu())

    elif query.data == "deposit":
        await query.edit_message_text("💰 Choose Payment Method:", reply_markup=deposit_menu())

    elif query.data == "filter":
        await query.edit_message_text("⚙ Select Filter:", reply_markup=filter_menu())

    elif query.data == "qr":
        await query.edit_message_text("📲 Send QR Code here...")

    elif query.data == "main":
        await query.edit_message_text("🏠 Main Menu", reply_markup=main_menu())

    elif query.data == "orders":
        await query.edit_message_text("📦 No orders yet.", reply_markup=main_menu())

    elif query.data == "balance":
        await query.edit_message_text("💰 Your balance: $0", reply_markup=main_menu())

    elif query.data == "support":
        await query.edit_message_text("🆘 Contact @support", reply_markup=main_menu())

# ================= RUN ================= #

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
