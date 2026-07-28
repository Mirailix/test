from mcpi import minecraft
import random
import time
# Подключение к Minecraft
mc = minecraft.Minecraft.create()

num_tiles = 6  # Всего плиток
tile_size = 4  # Размер каждой плитки

# Цвета шерсти (идентификаторы блоков)
colors = {
    "white": 0,
    "orange": 1,
    "gray": 7,
    "purple": 10,
    "blue": 11,
    "green": 13,
    "pink": 6,
}
available_colors = list(colors.keys())

pos = mc.player.getTilePos()
start_x = pos.x
start_y = pos.y + 100
start_z = pos.z

correct_color_name = random.choice(available_colors)
correct_color_id = colors[correct_color_name]
available_colors.remove(correct_color_name)

# Генерация плиток с цветами
tiles = [] # Список для хранения координат и ID
for i in range(num_tiles): # Каждая итерация создает одну плитку
    color = random.choice(available_colors) # Генерация случайного цвета
    available_colors.remove(color) # Удаляем использованный цвет
    color_id = colors[color] # Получаем дополнительный ID цвета
   
    # Расположение плиток: 3 плитки в ряд, 2 ряда
    row = i // 3  # Определяем ряд (0 или 1)
    col = i % 3   # Определяем колонку (0, 1 или 2)

    x = start_x + col * tile_size  # Позиция по X
    z = start_z + row * tile_size   # Позиция по Z
    # Создаем плитку
    for dx in range(tile_size): # Cмещение по оси X относительно начальной точки x
        for dz in range(tile_size): # Cмещение по оси Y относительно начальной точки y
            mc.setBlock(x + dx, start_y, z + dz, 35, color_id) # Установка блока
    tiles.append((x, start_y, z, color_id)) # Добавляем в список tiles

correct_tile_position = tiles[random.randint(0, num_tiles - 1)]
for dx in range(tile_size):
    for dz in range(tile_size):
        mc.setBlock(correct_tile_position[0] + dx, correct_tile_position[1],
                    correct_tile_position[2] + dz, 35, correct_color_id)

# Телепортируем Игрока на поле
mc.player.setTilePos(start_x + 3, start_y + 20, start_z + 3)

# Информируем игрока о начале игры
mc.postToChat("Find the " + correct_color_name)

# Ждем 5 секунд
for i in range(5, 0, -1):
    time.sleep(1)
    mc.postToChat(str(i))

# Удаляем все плитки, кроме правильной
for tile in tiles: # Перебор всех плиток
    if tile != correct_tile_position: # Если плитка НЕ правильная
        for dx in range(tile_size):
            for dz in range(tile_size):
                mc.setBlock(tile[0] + dx, tile[1], tile[2] + dz, 0)  


print("Игра завершена!") # Сообщение в консоль
