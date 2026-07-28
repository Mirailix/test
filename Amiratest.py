from mcpi.minecraft import Minecraft 
mc = Minecraft.create()

pos=mc.player.getTilePos()
x,y,z=pos.x, pos.y, pos.z # x=0 y=0 z=0

size=10
block=1

for i in range(size):
    mc.setBlocks(x, y+i, z, #x=0 y=1 z=0
                 x+size-1,y+i,z+size-1, #x=9 y=1 z=9
                 block)