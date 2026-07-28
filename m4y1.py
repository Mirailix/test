from mcpi.minecraft import Minecraft
import time
from unidecode import unidecode

# Подключение к Minecraft
mc = Minecraft.create()

file = 'test.txt' 

def handle_chat(event):
    chat_message = event.message.lower().strip() #!AdD = !add
   
    if chat_message.startswith('!add'): #Если введена команда !add
        text = chat_message[5:].strip()
        if text: #Если строка не пуста  
            file_write = open(file, 'a', encoding='utf-8') #Открываем файл
            file_write.write(f'\n - {text}') #Записываем дело
            message = "Дело добавлено!" #Сообщаем Игроку о выполнении
            mc.postToChat(unidecode(message)) #Отправляем в чат
        else: #Если сообщение пустое
            message = "Пожалуйста, укажите текст дела после команды !add" #Сообщщение для Игрока
            mc.postToChat(unidecode(message)) #Отправляем в чат
           
    elif chat_message == '!list': #Если введена команда !list
        # Выводим список дел
        file_open = open(file, 'r', encoding='utf-8') #Открываем файл
        lines = file_open.readlines()  # Читаем файл построчно
        for line in lines: #Проход по последовательности
            mc.postToChat(unidecode(line.rstrip())) #Отправляем в чат


while True: #Проверяет чат на предмет новых сообщений
    for post in mc.events.pollChatPosts():
        handle_chat(post) #Вызов функции обработки сообщений
       
    time.sleep(0.1) #Задержка