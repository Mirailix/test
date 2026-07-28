from mcpi import minecraft

mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()

FARM_START_X = pos.x
FARM_START_Y = pos.y
FARM_START_Z = pos.z
FARM_WIDTH = 10
FARM_LENGTH = 10

def make_farm():
    for x in range(FARM_WIDTH):
        for z in range(FARM_LENGTH):
            mc.setBlock(FARM_START_X + x, FARM_START_Y, FARM_START_Z + z, 60)
            if z % 2 == 0: 
                mc.setBlock(FARM_START_X + x, FARM_START_Y - 1, FARM_START_Z + z, 9)

def plant_seeds():
    while True:
        for x in range(FARM_WIDTH):
            for z in range(FARM_LENGTH):
                block_id = mc.getBlock(FARM_START_X + x, FARM_START_Y, FARM_START_Z + z)
               
                if block_id == 60:
                    above_block_id = mc.getBlock(FARM_START_X + x, FARM_START_Y + 1, FARM_START_Z + z)
                    if above_block_id == 0:  # Если над пахотной землёй воздух
                        # Высаживаем новое семя
                        mc.setBlock(FARM_START_X + x, FARM_START_Y + 1, FARM_START_Z + z, 59)
                        mc.postToChat(f"The seeds are planted in position")
                else:
                    mc.setBlock(FARM_START_X + x, FARM_START_Y, FARM_START_Z + z, 60)
                       
make_farm()
plant_seeds()
