"""筱羊冰冰制作的第一份闯关地图，初次尝试请多包含"""
import mcpi.minecraft as minecraft
import mcpi.block as block
import minecraftstuff
import time
from map1_func import *
mc = minecraft.Minecraft.create()
# 设置各个地方的坐标
pos_total = mc.player.getTilePos()
pos_check = pos_total.clone()
pos_maze = pos_total.clone()
pos_maze.x += 100
pos_maze.z += 100

pos_water = pos_total.clone()
pos_water.x += 100

pos_run = pos_total.clone()
pos_run.y += 100

pos_away = pos_total.clone()
pos_away.z += 100

pos_pyramid = pos_total.clone()
pos_pyramid.x -= 100
pos_pyramid.z -= 100
# 游戏状态，0表示还没结束，1表示结束了，2表示获得方块
game_stats = [1,1,1,1]

# build the home for player
build_home(pos_total)
build_maze(pos_maze)
build_water(pos_water)
build_run(pos_run)
build_away(pos_away)
build_pyramid(pos_pyramid)
while True:
    pos_now = mc.player.getTilePos()
    if pos_now.x  == pos_total.x+5 and pos_now.z == pos_total.z:
        # 可能存在重新玩，所以设置回去
        game_stats[0] = 0
        mc.player.setTilePos(pos_maze.x+1,pos_maze.y,pos_maze.z+1)
        # 迷宫尽头的坐标
        pos_end = pos_maze.clone()
        pos_end.x += 29
        pos_end.z += 28
        while not game_stats[0]:
            pos = mc.player.getTilePos()
            if pos.x == pos_end.x and pos.y == pos_end.y and pos.z == pos_end.z:
                game_stats[0] = 1
        else:
            mc.player.setTilePos(pos_total.x,pos_total.y,pos_total.z)
    elif pos_now.x  == pos_total.x and pos_now.z == pos_total.z+5:
        game_stats[1] = 0
        # 绘制跳台
        mc.setBlocks(pos_water.x-1,pos_water.y+50,pos_water.z-1,pos_water.x+1,pos_water.y+50,pos_water.z+1,block.GLASS.id)
        # 移动玩家
        mc.player.setTilePos(pos_water.x,pos_water.y+51,pos_water.z)
        time.sleep(3)
        # 撤除跳台
        mc.setBlocks(pos_water.x-1,pos_water.y+50,pos_water.z-1,pos_water.x+1,pos_water.y+50,pos_water.z+1,block.AIR.id)
        pos_end = pos_water.clone()
        pos_end.x += 10
        while not game_stats[1]:
            pos = mc.player.getTilePos()
            if pos.x == pos_end.x and pos.y == pos_end.y and pos.z == pos_end.z:
                game_stats[1] = 1
        else:
            mc.player.setTilePos(pos_total.x,pos_total.y,pos_total.z)
    elif pos_now.x  == pos_total.x and pos_now.z == pos_total.z-5:
        game_stats[2] = 0
        mc.player.setTilePos(pos_run.x+1,pos_run.y+1,pos_run.z+1)
        pos_end = pos_run.clone()
        pos_end.x += 15
        pos_end.z += 15
        pos_end.y += 50
        while not game_stats[2]:
            pos = mc.player.getTilePos()
            if pos.x == pos_end.x and pos.y == pos_end.y and pos.z == pos_end.z:
                game_stats[2] = 1
        else:
            mc.player.setTilePos(pos_total.x,pos_total.y,pos_total.z)
    elif pos_now.x  == pos_total.x-5 and pos_now.z == pos_total.z:
        game_stats[3] = 0
        mc.player.setTilePos(pos_run.x+1,pos.y+1,pos.z+1)
        pos_end = pos_away.clone()
        pos_end.x += 15
        pos_end.z += 15
        while not game_stats[3]:
            pos = mc.player.getTilePos()
            if pos.x == pos_end.x and pos.y == pos_end.y and pos.z == pos_end.z:
                game_stats[3] = 1
        else:
            mc.player.setTilePos(pos_total.x,pos_total.y,pos_total.z)
    
    if check(pos_check,game_stats):
        pos_end = pos_total.clone()
        pos_end.x += 25
        pos_end.y += 6
        while game_stats:
            pos = mc.player.getTilePos()
            if pos.x == pos_end.x and pos.y == pos_end.y and pos.z == pos_end.z:
                game_stats = None
        else:
            mc.player.setTilePos(pos_pyramid.x,pos_pyramid.y,pos_pyramid.z)
    
    if not game_stats:
        for i in range(9):
            width = 8-i
            mc.setBlocks(pos_pyramid.x-width,pos_pyramid.y+i,pos_pyramid.z-width,pos_pyramid.x+width,pos_pyramid.y+i,pos_pyramid.z+width,block.WATER.id)
            time.sleep(2)
