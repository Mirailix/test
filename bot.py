import telebot
import os
from dotenv import load_dotenv

# Загружаем токен из файла .env (рекомендуется для безопасности)

BOT_TOKEN = "8767799886:AAE_m9OdNN17u-fkceTejGcK0QjfvxNVS_U"


bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Привет! Я тестовый бот.\n"
                          "Отправь мне любое сообщение, и я его повторю.\n"
                          "Доступные команды: /start, /help")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "📖 Справка:\n"
                          "/start - запустить бота\n"
                          "/help - показать эту справку\n"
                          "Любой текст - бот его повторит")

# Обработчик всех остальных сообщений (эхо)
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, f"🔁 Вы написали: `{message.text}`", parse_mode="Markdown")

# Запуск бота
if __name__ == "__main__":
    print("✅ Бот запущен и ожидает сообщения...")
    # none_stop=True позволяет боту продолжать работу после ошибок сети
    bot.polling(none_stop=True)