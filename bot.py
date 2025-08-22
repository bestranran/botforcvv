# bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN, ADMIN_IDS
from database import get_balance, update_balance, add_product, get_available_product, mark_product_sold

# ------------------- 用户命令 -------------------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bal = get_balance(update.effective_user.id)
    await update.message.reply_text(f"💰 当前余额: {bal} 元")

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        new_bal = update_balance(update.effective_user.id, amount)
        await update.message.reply_text(f"💰 充值成功！当前余额: {new_bal} 元")
    except:
        await update.message.reply_text("❌ 命令格式错误，例如 /deposit 50")

async def addproduct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("❌ 无权限")
        return
    try:
        name = context.args[0]
        price = float(context.args[1])
        code = context.args[2]
        add_product(name, price, code)
        await update.message.reply_text(f"✅ 商品 {name} 添加成功")
    except:
        await update.message.reply_text("❌ 命令格式错误\n/add_product 名称 价格 卡料内容")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    product = get_available_product()
    if not product:
        await update.message.reply_text("❌ 库存不足")
        return
    if get_balance(user_id) < product['price']:
        await update.message.reply_text("❌ 余额不足，请先充值")
        return
    update_balance(user_id, -product['price'])
    mark_product_sold(product['id'])
    await update.message.reply_text(f"✅ 购买成功！\n商品：{product['name']}\n卡料：{product['code']}\n剩余余额：{get_balance(user_id)} 元")

# ------------------- 启动 Bot -------------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("deposit", deposit))
app.add_handler(CommandHandler("add_product", addproduct))
app.add_handler(CommandHandler("buy", buy))

print("Bot 已启动...")
app.run_polling()
