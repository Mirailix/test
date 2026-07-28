from mcpi import minecraft


# Подключение к Minecraft
mc = minecraft.Minecraft.create()


# Начальные координаты бота
bot_pos = mc.player.getTilePos()  # Копируем позицию игрока для начала


# Скорость движения бота (количество блоков за итерацию)
speed = 0.1


# Хранение предыдущей позиции бота
previous_pos = bot_pos.clone()


while True:
    # Получение текущих координат игрока
    player_pos = mc.player.getTilePos()
   
    # Вычисляем разницу между позицией игрока и позицией бота
    dx = player_pos.x - bot_pos.x
    dy = player_pos.y - bot_pos.y
    dz = player_pos.z - bot_pos.z
   
    # Вычисляем расстояние до игрока
    distance = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5


    # Если бот не на месте, перемещаем его
    if distance > 0:
        # Удаляем блок с предыдущей позиции бота
        mc.setBlock(int(previous_pos.x), int(previous_pos.y), int(previous_pos.z), 0)  # ID 0 - воздух


        # Перемещаем бота на заданную скорость
        bot_pos.x += dx * speed
        bot_pos.y += dy * speed
        bot_pos.z += dz * speed
       
        # Устанавливаем блок на позиции бота
        mc.setBlock(int(bot_pos.x), int(bot_pos.y), int(bot_pos.z), 41)


        # Обновляем предыдущую позицию бота
        previous_pos = bot_pos.clone()
