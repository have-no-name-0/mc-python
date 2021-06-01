"""the function used in map1"""
from math import fabs
import mcpi.minecraft as minecraft
import mcpi.block as block
import minecraftstuff
import random

mc = minecraft.Minecraft.create()
mcdrawding = minecraftstuff.MinecraftDrawing(mc)

# 随机生成四个孔
ls = []
i = 0
while i<4:
    pos = (random.randint(-9,9),random.randint(-9,9))
    if pos not in ls:
        ls.append([pos[0],9-max(abs(pos[0]),abs(pos[1])),pos[1]])
        i += 1

# 绘制新手村
def build_home(pos):
    mc.setBlocks(pos.x-20,pos.y-1,pos.z-20,pos.x+20,pos.y+10,pos.z+20,block.GOLD_BLOCK.id)
    mc.setBlocks(pos.x-19,pos.y,pos.z-19,pos.x+19,pos.y+9,pos.z+19,block.AIR.id)
    # 开一个天窗
    mcdrawding.drawHorizontalCircle(pos.x,pos.y+10,pos.z,5,block.AIR.id)

    # 设置几个游戏的开始地点
    pos_game1 = pos.clone()
    pos_game1.x += 5
    pos_game2 = pos.clone()
    pos_game2.z += 5
    pos_game3 = pos.clone()
    pos_game3.z -= 5
    pos_game4 = pos.clone()
    pos_game4.x -= 5

    mc.setBlock(pos_game1.x,pos_game1.y-1,pos_game1.z,block.DIAMOND_BLOCK.id)
    mc.setBlock(pos_game2.x,pos_game2.y-1,pos_game2.z,block.LAPIS_LAZULI_BLOCK.id)
    mc.setBlock(pos_game3.x,pos_game3.y-1,pos_game3.z,block.BEDROCK_INVISIBLE.id)
    mc.setBlock(pos_game4.x,pos_game4.y-1,pos_game4.z,block.IRON_BLOCK.id)
# 绘制迷宫
def build_maze(pos):
    with open("maze.csv") as fp:
        z = pos.z
        for line in fp.readlines():
            line = line.rstrip('\n')
            data = line.split(',')
            x = pos.x
            for d in data:
                if d == "1":
                    mc.setBlock(x,0,z,block.GOLD_BLOCK.id)
                    mc.setBlock(x,1,z,block.GOLD_BLOCK.id)
                    mc.setBlock(x,2,z,block.GOLD_BLOCK.id)
                x += 1
            z += 1
    # 放置特殊方块
    mc.setBlock(pos.x+23,-1,pos.z+1,block.DIAMOND_BLOCK.id)
    mc.setBlock(pos.x+29,-1,pos.z+28,block.GOLD_BLOCK.id)
# 绘制水立方
def build_water(pos):
    # 可供选择的方块列表，(id,data)
    ids = [(21,0), (30,0), (35,3), (35,5), (35,7), (35,8), (35,10), (78,0), (79,0)]
    # 四个指定方块，第一个是青金石，后三个是水
    water = []
    i = 0
    while i < 4:
        place = (random.randint(-4,5),random.randint(-4,5))
        for j in water:
            if place == j:
                break
        else:
            water.append(place)
            i += 1

    mc.setBlock(pos.x+water[0][0],pos.y,pos.z+water[0][1],block.LAPIS_LAZULI_BLOCK.id)
    mc.setBlock(pos.x+water[1][0],pos.y,pos.z+water[1][1],block.WATER.id)
    mc.setBlock(pos.x+water[2][0],pos.y,pos.z+water[2][1],block.WATER.id)
    mc.setBlock(pos.x+water[3][0],pos.y,pos.z+water[3][1],block.WATER.id)

    for i in range(-4,5):
        for j in range(-4,5):
            for k in water:
                if (i,j) == k:
                    break
            else:
                # 此处没有方块，需要放置
                block_id,block_data = random.choice(ids)
                mc.setBlock(pos.x+i,pos.y,pos.z+j,block_id,block_data)
                if block_id == 30:
                    # 30是蜘蛛网，下面配一个岩浆才刺激呢
                    mc.setBlock(pos.x+i,pos.y-1,pos.z+j,block.LAVA.id)
    mc.setBlock(pos.x+10,pos.y-1,pos.z,block.DIAMOND_BLOCK.id)

# 绘制跑酷
def build_run(pos):
    f = open("MazeMapOne.csv")
    ORIGIN_x = pos.x+1
    # y-3
    ORIGIN_y = pos.y-2
    ORIGIN_z = pos.z+1

    x,z = ORIGIN_x,ORIGIN_z

    for line in f.readlines():
        if line == '\n':
            ORIGIN_y += 1
            x = ORIGIN_x
            z = ORIGIN_z
            continue
        data = line.split(',')
        x = ORIGIN_x
        for cell in data:
            data_id,data_data = tuple(cell.split(' '))
            mc.setBlock(x,ORIGIN_y,z,int(data_id),int(data_data))
            x += 1
        z += 1
# 绘制解谜
def build_away(pos):
    f = open("MazeMapOne.csv")
    ORIGIN_x = pos.x+1
    # y-3
    ORIGIN_y = pos.y-2
    ORIGIN_z = pos.z+1

    x,z = ORIGIN_x,ORIGIN_z

    for line in f.readlines():
        if line == '\n':
            ORIGIN_y += 1
            x = ORIGIN_x
            z = ORIGIN_z
            continue
        data = line.split(',')
        x = ORIGIN_x
        for cell in data:
            data_id,data_data = tuple(cell.split(' '))
            mc.setBlock(x,ORIGIN_y,z,int(data_id),int(data_data))
            x += 1
        z += 1
# 绘制金字塔
def build_pyramid(pos):
    # 高十层
    for y in range(10):
        # 计算每一层到中轴线的距离
        width = 9-y
        # 分别绘制四条直线
        for x in range(pos.x-width,pos.x+width+1):
            mc.setBlock(x,pos.y+y,pos.z-width,block.GLASS.id)
            mc.setBlock(x,pos.y+y,pos.z+width,block.GLASS.id)
        for z in range(pos.z-width+1,pos.z+width):
            mc.setBlock(pos.x-width,pos.y+y,z,block.GLASS.id)
            mc.setBlock(pos.x+width,pos.y+y,z,block.GLASS.id)
    mc.setBlock(pos.x+ls[0][0],pos.y+ls[0][1],pos.z+ls[0][2],block.AIR.id)
    mc.setBlock(pos.x+ls[1][0],pos.y+ls[1][1],pos.z+ls[1][2],block.AIR.id)
    mc.setBlock(pos.x+ls[2][0],pos.y+ls[2][1],pos.z+ls[2][2],block.AIR.id)
    mc.setBlock(pos.x+ls[3][0],pos.y+ls[3][1],pos.z+ls[3][2],block.AIR.id)

# 检查是否开始最后的游戏
def check(pos,game_stats):
    game1 = mc.getBlock(pos.x+5,pos.y,pos.z)
    if game1 == block.DIAMOND_BLOCK.id:
        game_stats[0] = 2
    
    game2 = mc.getBlock(pos.x,pos.y,pos.z+5)
    if game2 == block.LAPIS_LAZULI_BLOCK.id:
        game_stats[1] = 2

    game3 = mc.getBlock(pos.x,pos.y,pos.z-5)
    if game3 == block.BEDROCK_INVISIBLE.id:
        game_stats[2] = 2

    game4 = mc.getBlock(pos.x-5,pos.y,pos.z)
    if game4 == block.IRON_BLOCK.id:
        game_stats[3] = 2
    if game_stats and sum(game_stats) == 8:
        build_stairs(pos)
        return True
    return False
# 建造通往最后的台阶
def build_stairs(pos):
    pos.x += 20
    mc.setBlocks(pos.x,pos.y,pos.z-5,pos.x,pos.y+10,pos.z+5,block.AIR.id)
    pos.y -= 1
    for i in range(5):
        pos.x += 1
        pos.y += 1
        mc.setBlocks(pos.x,pos.y,pos.z-5,pos.x,pos.y,pos.z+5,block.IRON_BLOCK.id)
    pos.y += 1
    mc.setBlock(pos.x,pos.y,pos.z,block.MOSS_STONE.id)
