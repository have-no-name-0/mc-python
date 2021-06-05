# -*- coding: utf-8 -*-  
from mcpi import minecraft,block
import pygame
import random

mc = minecraft.Minecraft.create()

pos = mc.player.getTilePos()
# 绘制界面，一个整体&四个边框
mc.setBlocks(pos.x-10,pos.y+1,pos.z+20,pos.x+10,pos.y+21,pos.z+20,block.STONE.id)
mc.setBlocks(pos.x-11,pos.y,pos.z+20,pos.x-11,pos.y+22,pos.z+20,block.GOLD_BLOCK.id)
mc.setBlocks(pos.x-10,pos.y,pos.z+20,pos.x+10,pos.y,pos.z+20,block.GOLD_BLOCK.id)
mc.setBlocks(pos.x-10,pos.y+22,pos.z+20,pos.x+10,pos.y+22,pos.z+20,block.GOLD_BLOCK.id)
mc.setBlocks(pos.x+11,pos.y,pos.z+20,pos.x+11,pos.y+22,pos.z+20,block.GOLD_BLOCK.id)

# 放置方向方块
mc.setBlock(pos.x-1,pos.y-1,pos.z,block.ICE.id)
mc.setBlock(pos.x+1,pos.y-1,pos.z,block.GLASS.id)
mc.setBlock(pos.x,pos.y-1,pos.z+1,block.LAPIS_LAZULI_BLOCK.id)
mc.setBlock(pos.x,pos.y-1,pos.z-1,block.IRON_BLOCK.id)

snakes = [(pos.x-9,pos.y+1),(pos.x-10,pos.y+1)]
tail = None
food = None
food_num = 1
game_stats = 1
direction = 0

direction_dic = {
    0:0,
    1:2,
    2:1,
    3:4,
    4:3
}
fclock = pygame.time.Clock()

def draw(snakes,food,tail):
    mc.setBlock(food[0],food[1],pos.z+19,block.DIAMOND_BLOCK.id)
    # 绘制蛇
    mc.setBlock(snakes[0][0],snakes[0][1],pos.z+19,block.END_STONE.id)
    for i in range(1,len(snakes)):
        mc.setBlock(snakes[i][0],snakes[i][1],pos.z+19,block.ICE.id)
    # 删除尾巴
    if tail:
        mc.setBlock(tail[0],tail[1],pos.z+19,block.AIR.id)

def new_food(snakes,pos):
    stats = True
    while(stats):
        position = (pos.x+random.randint(-10,10),pos.y+random.randint(1,21))
        if position not in snakes:
            return position

def get_direction(direction_dic, pos, direction):
    direction_arr = {
        (0, 1)  : 1,
        (0,-1)  : 2,
        (-1,0)  : 3,
        (1, 0)  : 4
    }
    mc = minecraft.Minecraft.create()
    new_pos = mc.player.getTilePos()
    help_arr = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    valid_tag = 0
    new_direction = (0,0)
    for i in help_arr:
        new_direction = i
        if new_pos.x == pos.x+i[0] and new_pos.z == pos.z+i[1]:
            valid_tag = 1
            break
    if valid_tag:
        if not direction:
            ret = 4
        else:
            if(direction_arr[new_direction] == direction_dic[direction]):
                ret = direction
            else:
                ret = direction_arr[new_direction]
    else:
        ret = direction
    return ret

def pirect(head,direction):
    direction_arr = {
        0 : (0, 0),
        1 : (0, 1),
        2 : (0,-1),
        3 : (-1,0),
        4 : (1, 0)
    }
    return (head[0]+direction_arr[direction][0], head[1]+direction_arr[direction][1])

food = new_food(snakes,pos)
draw(snakes,food,tail)

while(game_stats):
    direction = get_direction(direction_dic,pos,direction)
    pirect_pos = pirect(snakes[0],direction)
    if direction:
        if pirect_pos == food:
            # 吃到食物，将食物位置加进去就行
            snakes.insert(0,pirect_pos)
            food = None
            food_num += 1
        else:
            if pirect_pos[0] == pos.x-11 or pirect_pos[0] == pos.x+11 or pirect_pos[1] == pos.y or pirect_pos[1] == pos.y+22:
                # 出界
                game_stats = 0
                continue
            for i in snakes[1:-1]:
                # 碰到蛇身，但不是蛇尾
                if pirect_pos == i:
                    game_stats = 0
                    break
            else:
                tail = snakes.pop()
                snakes.insert(0,pirect_pos)
    if food == None:
        food = new_food(snakes,pos)
    draw(snakes,food,tail)
    
    fclock.tick(food_num)

for i in snakes:
    mc.setBlock(i[0],i[1],pos.z+19,block.AIR.id)