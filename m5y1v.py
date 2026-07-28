from mcpi.minecraft import Minecraft
import time


# Создаем объект Minecraft
mc = Minecraft.create()


# Задаем координаты области, которую будем отслеживать
x_min, x_max = 150, 155
y_min, y_max = 65, 70
z_min, z_max = -610, -600


# Основная функция для проверки положения игрока
def check_player_position():
    player_pos = mc.player.getTilePos()  # Получаем текущие координаты игрока
    x, y, z = player_pos.x, player_pos.y, player_pos.z # Разделяем координаты
   
    # Проверяем, находятся ли координаты внутри заданной области
    if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:
        print("Игрок вошел в область!")
        mc.postToChat("Welcome to the secret zone!")  # Сообщение в чат


# Основной цикл программы
while True:
    check_player_position()  # Проверяем положение игрока
    time.sleep(0.1)
