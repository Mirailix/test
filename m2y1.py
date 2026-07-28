# for i in range(11):
#     i = i * 7
#     print(i)
from mcpi.minecraft import Minecraft
mc = Minecraft.create()

for i in range(5):
    mc.postToChat(5*i)




