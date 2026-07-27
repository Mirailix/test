# class House:
#     def __init__ (self, id, xyz, depth):
#         self.id = id
#         self.xyz = xyz
#         self.depth = depth
        
#     def build(self):
#         for i in range(15):
#             mc.setBlock(xyz[0]+i,xyz[1],xyz[2],5)

#         for i in range(8):
#             mc.setBlock(xyz[0],xyz[1]+i,xyz[2],5)

#         for i in range(20):
#             mc.setBlock(xyz[0],xyz[1],xyz[2]+i,5)


# xyz=[100, 60, 70]
# print(xyz[2])

class People:
  
  def __init__(self,name,age):

    self.name = name 

    self.age = age


  def greetings(self):

    print(f"IH Welcome im {self.name}")


class Student(People):
        def info(self):
           print(f"Я студент!")

golem = Student("Golem", 10)
golem.greetings()
golem.info()
