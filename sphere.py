from mcpi.minecraft import Minecraft
mc = Minecraft.create()

pos = mc.player.getTilePos()
x, y, z = pos.x, pos.y+20, pos.z


# Параметры
R = 10 
block = 1 #id block

for x_pos in range(x - R, x + R + 1):
    for y_pos  in range(y - R, y + R + 1):
        for z_pos  in range(z - R, z + R + 1):
            # Рассчитываем расстояние от центра до текущей точки
            distance = ((x_pos - x)**2 + (y_pos - y)**2 + (z_pos - z)**2) ** 0.5# x^2+y^2+z^2=c^2
            # Если точка находится внутри сферы, ставим блок
            if distance <= R:
                mc.setBlock(x_pos, y_pos, z_pos, block)
