from mcpi import minecraft
import time

# Подключение к Minecraft
mc = minecraft.Minecraft.create()

#Расположение блока
x, y, z = 105, 81, 473 # Подставляете ваши координаты

# Устанавливаем начальный блок
mc.setBlock(x, y, z, 41)

# Бесконечный цикл для анимации
while True:
    # Перемещаем блок вправо
    mc.setBlock(x + 1, y, z, 41)  # Устанавливаем блок на новое место
    mc.setBlock(x, y, z, 0)  # Убираем блок с предыдущего места
    time.sleep(0.5)

    # Перемещаем блок влево
    mc.setBlock(x, y, z, 41)  # Устанавливаем блок обратно на исходное место
    mc.setBlock(x + 1, y, z, 0)  # Убираем блок с нового места
    time.sleep(0.5)

    mc.setBlock(x + 1, y+1, z, 41)  # Устанавливаем блок на новое место
    mc.setBlock(x+1, y, z, 0)  # Убираем блок с предыдущего места
    time.sleep(0.5)

    mc.setBlock(x+1, y, z, 41)  # Устанавливаем блок на новое место
    mc.setBlock(x+1, y+1, z, 0)  # Убираем блок с предыдущего места
    time.sleep(0.5)
