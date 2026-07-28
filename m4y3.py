class People:
    def __init__(self,name,age,job):
        self.name = name
        self.age = age
        self.job=job

    def greetings(self):
        print(f"{self.name}  говорит привет")

    def sayMyname(self):
        print(self.name)
    


class Student(People):
    def info(self):
        print(f'Привет меня зовут {self.name}')

    def Marks(self):
        print("Русский - 5 , Английский - кол")




anny=People("Anny",23)
print(anny.name,anny.age)
# anny.think()
anny.sayMyname()
anny.Marks()


# Leha1=Student("dahsdahsdh",25)
# Leha1.info()
# Leha1.think()
# Leha1.sayMyname()

from mcpi import minecraft
mc = minecraft.Minecraft.create()


class House:
    def __init__(self, x, y, z, width, depth, height, block):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.depth = depth
        self.height = height
        self.block = block


    def build(self):
        #Постройка пола и крыши
        for dx in range(self.width + 1):
            for dz in range(self.depth + 1):
                mc.setBlock(self.x + dx, self.y, self.z + dz, self.block)
                mc.setBlock(self.x + dx, self.y + self.height + 1, self.z + dz, self.block)
       
        #Постройка стен
        for dx in range(self.width + 1):
            for dy in range(self.height + 1):
                mc.setBlock(self.x + dx, self.y + dy, self.z, self.block)
                mc.setBlock(self.x + dx, self.y + dy, self.z + self.depth, self.block)


        for dz in range(1, self.depth):
            for dy in range(self.height + 1):
                mc.setBlock(self.x, self.y + dy, self.z + dz, self.block)
                mc.setBlock(self.x + self.width, self.y + dy, self.z + dz, self.block)


        #Отверстие для двери
        for i in range(2):
            mc.setBlock(self.x + self.width // 2, self.y + 1 + i, self.z, 0)  

class Church(House):
    def make_church(self):
         # Строим башню
        for dx in range(self.width - 1):
            for dz in range(self.depth - 1):
                for dy in range(3):
                    mc.setBlock(self.x + 1  + dx, self.y + self.height + 2 + dy, self.z + 1  + dz, self.block - 1)
        
        # Добавляем крест на крыше
        cross_x = self.x + (self.width // 2)  # Центр по x
        cross_z = self.z + (self.depth // 2)   # Центр по z
       
        for i in range(3): #Строим вертикальную линию
            mc.setBlock(cross_x, self.y + self.height + i + 5, cross_z, self.block)


        mc.setBlock(cross_x + 1, self.y + self.height + 6, cross_z, self.block) #Строим горизонтальный блок 1
        mc.setBlock(cross_x - 1, self.y + self.height + 6, cross_z, self.block) #Строим горизонтальный блок 2




player_pos = mc.player.getTilePos()
house = House(player_pos.x, player_pos.y, player_pos.z, 8, 6, 5, 42)
house.build()

player_pos = mc.player.getTilePos()
house = Church(player_pos.x, player_pos.y, player_pos.z, 8, 6, 5, 42)
house.build()
house.make_church()




