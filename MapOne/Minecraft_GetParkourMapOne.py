import mcpi.minecraft as minecraft

mc = minecraft.Minecraft.create()

filename = "MazeMapOne.csv"

sizex = 30 #长30
sizey = 9  #高9
sizez = 30 #宽30

def scan(filename, originx, originy, originz):
    with open (filename, "w") as f:
        for y in range(-3,7):
            f.write("\n")   #层
            for x in range(sizex):
                line = []   #行
                for z in range(sizez):
                    block = mc.getBlockWithData(originx+x, originy+y, originz+z) #块
                    line.append(str(block.id)+' '+str(block.data))
                f.write(",".join(line) + "\n")

pos = mc.player.getTilePos() #坐标底层中点
scan(filename, pos.x-(sizex/2)+1, pos.y, pos.z-(sizez/2)+1) #逐层扫描地图