class figure:
    def __init__(self, sidelength):
        self.sidelength = sidelength

    def say(self):
        print(f"у квадрата сторона = {self.sidelength} см")  

    def Perimetr(self):
        print(f"Периметр квадара = {self.sidelength*4}")


square =figure(20)
square.Perimetr()