import mcpi.minecraft as minecraft
import mcpi.block as block

mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()

door_x = 736  
door_y = 65
door_z = 435

def create_door():
    mc.setBlock(door_x, door_y, door_z, block.WOOD)  # Нижний блок двери
    mc.setBlock(door_x, door_y + 1, door_z, block.WOOD)  # Верхний блок двери

# Функция для удаления двери
def remove_door():
    mc.setBlock(door_x, door_y, door_z, block.AIR)  # Удалить нижний блок двери
    mc.setBlock(door_x, door_y + 1, door_z, block.AIR)  # Удалить верхний блок двери

# Создаем дверь в начале
create_door()

# Основной цикл
while True:
    player_pos = mc.player.getTilePos() # Получение текущей позиции игрока
   
    # Проверяем расстояние до двери
    distance = ((player_pos.x - door_x) ** 2 + (player_pos.z - door_z) ** 2) ** 0.5 # (a^2 + b^2)^0.5
   
    if distance < 5:  # Если игрок близко к двери (дальность можно увеличить)
        remove_door()  # Удаляем дверь
    else:
        # Проверяем состояние двери и восстанавливаем ее только если она была удалена
        if mc.getBlock(door_x, door_y, door_z) == block.AIR.id:
            create_door()  # Восстанавливаем дверь, если игрок далеко
