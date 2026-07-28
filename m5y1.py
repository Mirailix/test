from mcpi.minecraft import Minecraft
mc = Minecraft.create()

tnt_id = 46

last_blocks = {}

# Основной цикл программы
while True:
    # Получаем все блоки вокруг игрока
    player_pos = mc.player.getTilePos()
    for dx in range(-1, 2):  # Проверяем блоки вокруг игрока (3x3)
        for dz in range(-1, 2):
            x = player_pos.x + dx
            z = player_pos.z + dz
            y = player_pos.y  # Проверяем на том же уровне Y

            # Получаем ID блока
            block_id = mc.getBlock(x, y, z)

            # Проверяем, изменился ли блок
            if (x, y, z) not in last_blocks or last_blocks[(x, y, z)] != block_id:
                last_blocks[(x, y, z)] = block_id  # Обновляем ID блока

                if block_id == tnt_id:
                    print("Предупреждение: Игрок поставил динамит! Координаты:", (x, y, z))
                    mc.postToChat("Attention! The use of dynamite is prohibited!")  # Сообщение в чат
                    mc.setBlock(x,y,z,0)


