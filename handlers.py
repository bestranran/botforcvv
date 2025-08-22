from telegram import Update
from telegram.ext import ContextTypes
from database import get_conn
from keyboards import main_menu
from datetime import datetime
from config import ADMIN_IDS

# 用户逻辑
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?,?)", (user_id, username))
    conn.commit()
    conn.close()
    await update.message.reply_text("欢迎使用卡料商店Bot！", reply_markup=main_menu())

# 回调按钮处理
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 类似之前 bot.py 的 button() 函数
    pass

# 充值处理
async def deposit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

# 管理端装饰器
def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("❌ 你没有权限")
            return
        await func(update, context)
    return wrapper

# 管理员命令示例
@admin_only
async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass
