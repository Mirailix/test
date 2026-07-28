import cv2
import numpy as np
from mcpi import minecraft
# Подключаемся к Minecraft
mc = minecraft.Minecraft.create()

# Определение соответствия цветов к блокам Minecraft
color_to_block = {
    (0, 0, 0): 1, # Red Green Blue RGB
    (255, 255, 255): 35,
    (128, 128, 128): 1,  
    (214,111,32): 3,
    (186,67,35): 24,
}

# Функция для нахождения ближайшего цвета
def find_closest_color(color):
    min_diff = float('inf')
    closest_color = None
    for c in color_to_block.keys():
        diff = np.linalg.norm(np.array(color) - np.array(c))
        if diff < min_diff:
            min_diff = diff
            closest_color = c

image_path = 'leather.jpg' # Замените на путь к вашему изображению
image = cv2.imread(image_path)

scale_factor = min(64 / image.shape[0], 64 / image.shape[1])
new_size = (int(image.shape[1] * scale_factor), int(image.shape[0] * scale_factor))
pixel_art = cv2.resize(image, new_size, interpolation=cv2.INTER_NEAREST)
pixel_art_colors = [] 
for row in pixel_art: 
    pixel_row = []
    for pixel in row:
        closest_color = find_closest_color(pixel) # Находим наиболее близкий цвет
        pixel_row.append(closest_color) # Обработанный пиксель добавляется в строку
        print(f"Обрабатываем цвет: {pixel}, ближайший цвет: {closest_color}")  # Отладочная информация
    pixel_art_colors.append(pixel_row) # Результат добавляется в общий список

#Определение стартовой позиции
pos = mc.player.getTilePos()
start_x = pos.x + 2
start_y=pos.y
start_z=pos.z

for y in range(len(pixel_art_colors)):
    for x in range(len(pixel_art_colors[y])):
        block_color = pixel_art_colors[y][x]
        block_id = color_to_block.get(block_color)

        if block_id is not None:
            mc.setBlock(start_x+x,start_y+y,start_z+y,block_id)
        else:
            print(f"Цвет {block_color} не найден в словаре блоков")

print("Отрисовка завершена")

