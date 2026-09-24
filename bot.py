import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# =====================================================================
# НАСТРОЙКИ БОТА: Обязательно заполните эти три строчки!
# =====================================================================
TOKEN = "7982800755:AAFR7j6zopjaapbRmPE6l-aQQF4iDPLfho8"  # Длинный API токен от @BotFather
ADMIN_ID = 5553501056             # Ваш личный ID в Telegram, чтобы бот присылал вам заказы
NETLIFY_URL = "https://marvelous-chebakia-bb604d.netlify.app/"  # Ваша ссылка на Mini App от Netlify Drop
# =====================================================================

# Настройка логирования, чтобы видеть ошибки в консоли
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение при отправке /start."""
    user_name = update.effective_user.first_name
    
    # Создаем нативную инлайн-кнопку со встроенным Mini App
    keyboard = [[InlineKeyboardButton(text="🛍️ Открыть XS OUTFIT", web_app=WebAppInfo(url=NETLIFY_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"Привет, {user_name}! 👋\n\n"
        "Добро пожаловать в официальный бот премиальной мужской одежды **XS OUTFIT**.\n\n"
        "Нажмите на кнопку ниже, чтобы открыть наш концептуальный магазин, изучить новые дропы и оформить заказ."
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def web_app_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ловит данные заказа, которые отправляет фронтенд через tg.sendData()."""
    # Текст заказа, собранный JavaScript-кодом в приложении
    order_data = update.effective_message.web_app_data.data
    user = update.effective_user
    
    # 1. Отправляем красивый чек самому покупателю в чат
    client_message = (
        "✅ **Заказ успешно отправлен!**\n\n"
        f"{order_data}\n"
        "⏳ Наш менеджер уже проверяет наличие размеров на складе и свяжется с вами в личных сообщениях в течение 10 минут.\n\n"
        "Спасибо, что выбираете XS OUTFIT! 🔥"
    )
    await update.message.reply_text(client_message, parse_mode="Markdown")
    
    # 2. Формируем подробную карточку уведомления для ВАС (администратора)
    admin_message = (
        "🚨 **НОВЫЙ ЗАКАЗ В XS OUTFIT!**\n\n"
        f"👤 **Покупатель:** {user.first_name} {user.last_name or ''}\n"
        f"🏷️ **Юзернейм:** @{user.username or 'скрыт'}\n"
        f"🆔 **Telegram ID:** `{user.id}`\n\n"
        f"{order_data}"
    )
    
    try:
        # Бот пересылает чек админу по его ID
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Не удалось отправить уведомление администратору: {e}")

def main():
    """Запуск и инициализация бота."""
    app = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков команд и событий
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data_handler))
    
    print("Бот XS OUTFIT успешно запущен и слушает входящие заказы...")
    app.run_polling()

if __name__ == '__main__':
    main()
