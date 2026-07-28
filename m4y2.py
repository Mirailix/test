from mcpi import minecraft
import pickle
mc = minecraft.Minecraft.create()

def copy_structure(start_pos, size): # x= 15 y=8 z= 10
    structure = [] # Список для информации о блоках
    for x in range(size[0]): # Проходимся по всем блокам в ширину
        for y in range(size[1]): # Проходимся по всем блокам в высоту
            for z in range(size[2]): # Проходимся по всем блокам в глубину
                # Получение информации о блоке
                block_id = mc.getBlock(start_pos[0] + x, start_pos[1] + y, start_pos[2] + z)
                if block_id != 0:  # Проверяем, что блок не воздух
                    structure.append(((x, y, z), block_id)) # Добавление блока в структуру
    return structure # Возвращение результата


# Функция для выгрузки конструкции
def paste_structure(structure, target_pos):
    for (x, y, z), block_id in structure: # Перебор элементов структуры
        # Ставим блок
        mc.setBlock(target_pos[0] + x, target_pos[1] + y, target_pos[2] + z, block_id)


# Получаем позицию игрока
player_pos = mc.player.getTilePos()
start_pos = (player_pos.x - 1, player_pos.y, player_pos.z - 1)  # Начальная позиция
size = (17, 25, 6)  # Размер конструкции (ширина, высота, глубина)


# Копируем конструкцию
structure = copy_structure(start_pos, size)
print("Конструкция скопирована!")

# Сохраняем конструкцию в файл
file = open('structure.pkl', 'wb')
pickle.dump(structure, file)
print("Конструкция сохранена!")


# Загружаем конструкцию из файла
file = open('structure.pkl', 'rb')
loaded_structure = pickle.load(file)
print("Конструкция загружена!")


# Вставляем конструкцию на новое место
input("Нажми Enter в консоли, чтобы вставить сюда конструкцию") # Получаем подтверждение о вставке на данное место
player_pos = mc.player.getTilePos() # Получаем позицию игрока
target_pos = (player_pos.x, player_pos.y, player_pos.z) # Список координат для вставки


#Вставляем конструкцию из файла
paste_structure(loaded_structure, target_pos)
print("Конструкция вставлена!")



