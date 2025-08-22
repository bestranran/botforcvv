from telegram import Update
from telegram.ext import CallbackContext
from database import *
from config import ADMIN_IDS
from keyboards import main_menu, country_menu, category_menu, products_menu

# --------------------- 用户命令 ---------------------
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    add_user(user.id, user.username)
    update.message.reply_text("欢迎来到卡料商店！请选择功能：", reply_markup=main_menu())

# --------------------- 按钮点击 ---------------------
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    # 查询余额
    if query.data == "balance":
        user = get_user(user_id)
        query.edit_message_text(f"💰 你的余额: {user['balance']} 元", reply_markup=main_menu())

    # 用户充值
    elif query.data == "deposit":
        query.edit_message_text("请输入充值金额：")
        context.user_data['awaiting_deposit'] = True

    # 用户订单
    elif query.data == "orders":
        orders = list_orders(user_id)
        if not orders:
            text = "你还没有购买记录"
        else:
            text = "\n".join([f"{o['product_name']} - {o['code']}" for o in orders])
        query.edit_message_text(text, reply_markup=main_menu())

    # 圈子库
    elif query.data == "circle":
        countries = ["中国", "美国", "日本"]
        query.edit_message_text("选择国家：", reply_markup=country_menu(countries))

    # 国家分类
    elif query.data.startswith("country_"):
        country = query.data.split("_",1)[1]
        categories = ["手机号","邮箱","游戏号"]
        query.edit_message_text(f"选择 {country} 分类：", reply_markup=category_menu(country, categories))

    # 商品列表
    elif query.data.startswith("cat_"):
        _, country, category = query.data.split("_",2)
        products = get_products_by_country_category(country, category)
        query.edit_message_text(f"{country} - {category} 商品列表：", reply_markup=products_menu(products))

    # 购买商品
    elif query.data.startswith("buy_"):
        product_id = int(query.data.split("_")[1])
        user = get_user(user_id)
        product = [p for p in list_products() if p['id']==product_id][0]
        stock_item = get_stock(product_id)
        if not stock_item:
            query.edit_message_text("❌ 库存不足", reply_markup=main_menu())
            return
        if user['balance'] < product['price']:
            query.edit_message_text("❌ 余额不足，请先充值", reply_markup=main_menu())
            return
        # 扣款 + 发货
        update_balance(user_id, -product['price'])
        mark_stock_sold(stock_item['id'])
        add_order(user_id, product_id, stock_item['code'])
        query.edit_message_text(
            f"✅ 购买成功！\n商品：{product['name']}\n卡料内容：{stock_item['code']}\n剩余余额：{user['balance']-product['price']} 元",
            reply_markup=main_menu()
        )

# --------------------- 用户输入消息 ---------------------
def message_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text
    if context.user_data.get('awaiting_deposit'):
        try:
            amount = float(text)
            update_balance(user_id, amount)
            update.message.reply_text(f"💰 充值成功！当前余额: {get_user(user_id)['balance']} 元", reply_markup=main_menu())
        except:
            update.message.reply_text("❌ 输入金额无效", reply_markup=main_menu())
        context.user_data['awaiting_deposit'] = False

# --------------------- 管理员命令 ---------------------
def admin_add_product(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        update.message.reply_text("❌ 无权限")
        return
    try:
        name = context.args[0]
        price = float(context.args[1])
        country = context.args[2]
        category = context.args[3]
        add_product(name, price, country, category)
        update.message.reply_text(f"✅ 商品 {name} 添加成功")
    except:
        update.message.reply_text("❌ 命令格式错误\n/add_product 名称 价格 国家 分类")

def admin_list_products(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        update.message.reply_text("❌ 无权限")
        return
    products = list_products()
    text = "\n".join([f"{p['id']}. {p['name']} {p['price']}元 ({p['country']}/{p['category']})" for p in products])
    update.message.reply_text(text if text else "暂无商品")
