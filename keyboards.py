from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 我的余额", callback_data="balance")],
        [InlineKeyboardButton("🛒 圈子库", callback_data="circle")],
        [InlineKeyboardButton("➕ 充值", callback_data="deposit")],
        [InlineKeyboardButton("📦 我的订单", callback_data="orders")]
    ]
    return InlineKeyboardMarkup(keyboard)

def country_menu(countries):
    keyboard = [[InlineKeyboardButton(c, callback_data=f"country_{c}")] for c in countries]
    return InlineKeyboardMarkup(keyboard)

def category_menu(country, categories):
    keyboard = [[InlineKeyboardButton(c, callback_data=f"cat_{country}_{c}")] for c in categories]
    return InlineKeyboardMarkup(keyboard)

def products_menu(products):
    keyboard = [[InlineKeyboardButton(f"{p['name']} {p['price']}元", callback_data=f"buy_{p['id']}")] for p in products]
    return InlineKeyboardMarkup(keyboard)
