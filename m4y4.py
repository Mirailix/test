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