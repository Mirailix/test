from mcpi import minecraft

mc = minecraft.Minecraft.create()

blocks = [14, 15, 16, 56, 129]  # Золото, Железо, Уголь, Алмазы, Изумруды

while True:

    pos = mc.player.getTilePos()
       
    for depth in range(1, 21):
        block_below = mc.getBlock(pos.x, pos.y - depth, pos.z)
        block_x= mc.getBlock(pos.x, pos.y + depth, pos.z)

        if block_below in blocks:
            mc.postToChat(f"Block ID: ({block_below}). Depth: {depth}")
            break

        if block_x in blocks:
            mc.postToChat(f"Block ID: ({block_x}). Nad Toboi: {depth}")
            break   
