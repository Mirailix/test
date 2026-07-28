from mcpi import minecraft
import time

mc = minecraft.Minecraft.create()
# Получаем позицию старта
x, y, z = 32, 63, 215  # подставьте свои координаты

while True:
    for i in range(5):  # Длина (2 блока)
        for j in range(2):  # Ширина (2 блока)
            mc.setBlock(x + j, y, z + i, 51)
   
    time.sleep(3)  
    
    for i in range(2):  
        for j in range(2):  
            mc.setBlock(x + j, y, z + i, 0)  
   
    time.sleep(1)  


# from mcpi import minecraft
# import time

# # Подключение к Minecraft
# mc = minecraft.Minecraft.create()

# block_x, block_y, block_z = 295, 64, 93 # Подставляете ваши координаты

# # Задаем координаты, куда будет телепортирован игрок
# teleport_x, teleport_y, teleport_z = 295, 100, 93

# while True:
#     # Получаем текущую позицию игрока
#     player_pos = mc.player.getTilePos()
 
#     # Проверяем, находится ли игрок на позиции блока
#     if (player_pos.x == block_x) and (player_pos.y == block_y + 1) and (player_pos.z == block_z):
#         # Телепортируем игрока на заданные координаты
#         mc.player.setTilePos(teleport_x, teleport_y, teleport_z)
#         time.sleep(1) # Ждем 1 секунду, чтобы избежать многократного телепорта


