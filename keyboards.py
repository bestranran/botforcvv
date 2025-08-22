from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 我的余额", callback_data="balance")],
        [InlineKeyboardButton("🛒 圈子库", callback_data="circles")],
        [InlineKeyboardButton("➕ 充值", callback_data="deposit")],
        [InlineKeyboardButton("📦 我的订单", callback_data="my_orders")]
    ]
    return InlineKeyboardMarkup(keyboard)
