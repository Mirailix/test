from mcpi.minecraft import Minecraft 
import time
mc = Minecraft.create()
mc.postToChat(2+2)
mc.postToChat(2+2)

a=123
b=656


if a>b:
    mc.postToChat("a больше b")
else:
    mc.postToChat("b больше a")


print(a+b)
print(a*b)
print(a/b)
print(a-b)
mc.player.getTilePos()
mc.player.getTilePos()
#time.sleep(3)
#mc.player.setTilePos(1000,72,56)
#time.sleep(3)
#mc.player.setTilePos(131,233,80)



mc.setBlock(768,63,374,49)
x=768
y=63
z=374
for i in range(5):
    mc.setBlock(x,y+i,z,49)

mc.setBlock(x,y+4,z+1,49)
mc.setBlock(x,y+4,z+2,49)

for i in range(5):
    mc.setBlock(x,y+i,z+2,49)

mc.setBlock(x,y,z+2,49)