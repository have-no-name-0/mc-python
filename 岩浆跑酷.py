# 开始前，玩家在一块固定位置的石块上，同时生成第一周期的石块。直到玩家跳到第一周期的石块，初始石块才消失
# 玩家跳到第一周期的石块后，初始石块消失，生成下一周期石块，并开始计时。玩家需要在规定时间内及时跳到下一周期的石块。

# 为了便于区分，可以让不同周期的石块呈现不同的颜色
# 场上总是只存在两个周期的石块
# 玩家跳到一个石块后，下周期石块出现，本周期其他石块暂不消失。但计时达到阈值，则本周期其他石块消失

# 初始位置在岩浆池中心上方6个单位高度处(25, 6, 25) 
# 岩浆池为边长为51的正方形
from random import randint
from mcpi import minecraft

# 判断新位置的合法性，即在X-Z方向的投射在岩浆池内，且石块的Y坐标在岩浆池之上
# pos为3元组，分别表示 X, Z, Y 坐标
def valid_judge(absolute_pos, origin_pos):
    if(absolute_pos[0] > origin_pos[0]+7 or absolute_pos[0] < origin_pos[0]-7 or absolute_pos[1] > origin_pos[1]+7 or absolute_pos[1] < origin_pos[1]-7 or absolute_pos[2] <= 0):
        return 0
    else:
        return 1

# 玩家失败判断
def fail_judge(player_pos, origin_pos):
    return not valid_judge(player_pos, origin_pos)

# 判断玩家是否跳到了新位置（下个周期的4个石块位置之一）
def get_newpos_judge(player_pos, new_list):
    for i in new_list:
        if player_pos[0] == i[0] and player_pos[1] == i[1] and player_pos[2] == i[2]+1:
            return 1
    return 0

# 判断一个位置是否与旧列表中的位置重合
def noRepeatJudge(old_list, absolute_pos):
    for i in old_list:
        if i == absolute_pos:
            return False
    return True

# 根据跳到新的位置后，根据这个位置生成下一个周期的4个石块的位置
def newPosGenerate(old_list, player_pos, origin_pos, cnt, list_length):
    new_list = []     
    i = 0
    while i < list_length:
        relative_x = randint(-3, 3)
        relative_z = randint(-3, 3)
        if cnt > 5:
            relative_y = randint(-2, 0)
        else: 
            relative_y = -1

        relative_pos = (relative_x, relative_z, relative_y)# 相对位置
        # 绝对位置
        absolute_pos = (player_pos[0] + relative_pos[0], player_pos[1] + relative_pos[1], player_pos[2] + relative_pos[2])
        if valid_judge(absolute_pos, origin_pos):       # 绝对位置合法性判断
            if noRepeatJudge(old_list, absolute_pos):   # 绝对位置不与旧列表中的位置重合
                new_list.append(absolute_pos)
                i = i + 1
    return new_list

# 将列表中的位置对应的块换成空气
def clearBlocks(ls):
    for i in ls:
        print(i)
        mc.setBlock((i[0], i[2], i[1]), 0)   # 将之前的块变为空气




from mcpi import minecraft
import random

mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()
# pos = mc.player.getTilePos()          # 获得玩家位置
origin_pos = (pos.x,pos.z,6)            # 位置参数转移
player_pos = origin_pos


mc.setBlocks(pos.x-7, -1, pos.z-7, pos.x+8, -1, pos.z+8, 9) # 挖坑（放水）
mc.setBlock(pos.x, -2, pos.z, 35, 1)                        # 中心位置标记
mc.setBlock(pos.x, 5, pos.z, 35, 0)                         # 设置白色羊毛块
print(pos.x, 5, pos.z)
mc.player.setTilePos(pos.x, 6, pos.z)                       # 把玩家拉到起始点
old_list = [(pos.x, pos.z, 5), (pos.x, pos.z, 5), (pos.x, pos.z, 5), (pos.x, pos.z, 5)]
new_list = []
fail_flag   = 0
list_length = 4
wool_color  = 0
cnt         = 0

clearFlag = 0   # 失败后清除石块标志

while True:
    
    while not fail_flag:
        print(old_list,new_list)
        # 获取新块位置并设置新块
        new_list = newPosGenerate(old_list, player_pos, origin_pos, cnt, list_length)
        wool_color = 0 if wool_color == 15 else wool_color+1
        for i in range(0, list_length):
            mc.setBlock(new_list[i][0], new_list[i][2], new_list[i][1], 35, wool_color)

        # 等待玩家跳到新块上或失败
        new_pos = mc.player.getTilePos()                # 获得玩家位置
        player_pos = (new_pos.x,new_pos.z,new_pos.y)    # 位置参数转移
        while not fail_flag and not get_newpos_judge(player_pos, new_list):
            new_pos = mc.player.getTilePos()                # 获得玩家位置
            player_pos = (new_pos.x,new_pos.z,new_pos.y)    # 位置参数转移
            fail_flag = fail_judge(player_pos, origin_pos)
    
        # 如果成功跳到新快上
        if not fail_flag:
            """
            for i in old_list:
                mc.setBlock((i[0], i[2], i[1]), 0)   # 将之前的块变为空气   
            """
            cnt = cnt + 1
            clearBlocks(old_list)           # 将之前的块变为空气
            for i in range(0, 4):
                old_list[i] = new_list[i]   # 将新块转移到旧块
        else:
            clearFlag = 1

    # print("fail_flag = ", fail_flag)
    
    # 清除石块标志
    if clearFlag:
        clearBlocks(old_list)
        clearBlocks(new_list)
        old_list = [(pos.x, 5, pos.z), (pos.x, 5, pos.z), (pos.x, 5, pos.z), (pos.x, 5, pos.z)]
        clearFlag = 0

    # 失败后持续监测玩家位置
    if fail_flag:
        new_pos = mc.player.getTilePos()                # 获得玩家位置
        player_pos = (new_pos.x,new_pos.z,new_pos.y)    # 位置参数转移
        if player_pos[0] == origin_pos[0] and player_pos[1] == origin_pos[1]:
            fail_flag = 0
            cnt = 0
            mc.setBlock(pos.x, 5, pos.z, 35, 0)                         # 设置白色羊毛块
            mc.player.setTilePos(origin_pos[0], 6, origin_pos[1])       # 把玩家拉到起始点
            player_pos = (player_pos[0], player_pos[1], 6)


"""
old_list = [(25, 6, 25), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
origin_pos = (25, 6, 25)    # 初始位置
cnt = 0     # 生成次数
lava_y = 0  # 岩浆所在的高度
length = 50 # 岩浆池长度
width = 50  # 岩浆池宽度
new_list = function(player_pos, cnt)

if get_newpos_judge(player_pos, new_list):
    for i in range(0, 4):
        old_list[i] = new_list[i]
"""




    