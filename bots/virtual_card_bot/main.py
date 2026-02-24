import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# ---------- MAIN MENU ----------
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, edit=False):
    keyboard = [
        [InlineKeyboardButton("🛍 Buy Card", callback_data="buy")],
        [InlineKeyboardButton("🏪 Sites List", callback_data="sites")],
        [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("📊 Balance", callback_data="balance")],
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
    ]

    text = (
        "★彡━━━━━━━━━━━━彡★\n"
        "🚀 𝗩𝗲𝗹𝘁𝗿𝗶𝘅 𝗣𝗮𝘆𝗖𝗼𝗿𝗲 v4.1\n"
        "Premium Automation System\n"
        "★彡━━━━━━━━━━━━彡★\n\n"
        "Select an option:"
    )

    if edit:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await main_menu(update, context)


# ---------- SITES ----------
async def sites_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 MyPrepaidCenter", callback_data="listings")],
        [InlineKeyboardButton("💳 BalanceNow", callback_data="listings")],
        [InlineKeyboardButton("🎁 VanillaGift", callback_data="listings")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
    ]

    await update.callback_query.edit_message_text(
        "🏪 Gift Cards Exchange - Sites List\n\nSelect Site:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------- LISTINGS ----------
async def listings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1️⃣ $50 | 38%", callback_data="purchase")],
        [InlineKeyboardButton("2️⃣ $100 | 35%", callback_data="purchase")],
        [InlineKeyboardButton("3️⃣ $250 | 30%", callback_data="purchase")],
        [InlineKeyboardButton("⬅ First Page", callback_data="page_first"),
         InlineKeyboardButton("➡ Next", callback_data="page_next")],
        [InlineKeyboardButton("🎛 Filter", callback_data="filter")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_sites")]
    ]

    await update.callback_query.edit_message_text(
        "📄 Listings Page 1\n\nSelect Card:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------- FILTER ----------
async def filter_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("<= $50", callback_data="filter_50"),
         InlineKeyboardButton("<= $100", callback_data="filter_100")],
        [InlineKeyboardButton("> $100", callback_data="filter_high")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_listings")]
    ]

    await update.callback_query.edit_message_text(
        "🎛 Filter Cards:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------- DEPOSIT ----------
async def deposit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Generate Stripe Link", callback_data="stripe_link")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
    ]

    await update.callback_query.edit_message_text(
        "💰 Deposit Funds\n\nChoose payment method:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------- CALLBACK ROUTER ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "buy":
        await sites_menu(update, context)

    elif data == "sites":
        await sites_menu(update, context)

    elif data == "listings":
        await listings_menu(update, context)

    elif data == "filter":
        await filter_menu(update, context)

    elif data == "deposit":
        await deposit_menu(update, context)

    elif data == "balance":
        await query.edit_message_text(
            "📊 Account Balance: $0.00",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]])
        )

    elif data == "back_main":
        await main_menu(update, context, edit=True)

    elif data == "back_sites":
        await sites_menu(update, context)

    elif data == "back_listings":
        await listings_menu(update, context)

    elif data == "refresh":
        await main_menu(update, context, edit=True)

    elif data == "purchase":
        await query.edit_message_text(
            "🛒 Purchase Confirmed!\n\nCard will be delivered after payment.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]])
        )

    elif data == "stripe_link":
        await query.edit_message_text(
            "🔗 Stripe Payment Link:\n\nhttps://stripe-link-here.com",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]])
        )


# ---------- APP ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
