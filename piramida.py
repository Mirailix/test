from mcpi.minecraft import Minecraft 
mc = Minecraft.create() 

pos = mc.player.getTilePos() # Создаём объект класса Minecraft
x, y, z = pos.x, pos.y, pos.z # Получаем позицию игрока

size = 10
block = 1

for i in range(size): # Цикл, проходящий по слоям сверху вниз
    mc.setBlocks(x, y + i, z, #x=0 y=1 z=0
                 x + size, y + i, z + size, # x=10 y=1 z=10
                 block)
    
