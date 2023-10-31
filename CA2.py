import pygame
import os
import _thread
pygame.init()

screenx, screeny = 1152, 896

length = 64

world = dict()

origin = [0,0] #本质上是（0，0）点的实际坐标


"""
def track():
    #用中位数确定中心点
    tmp = world.keys()
    tmpx, tmpy = list(), list() #分别包含所有横纵坐标的值
    for i in tmp:
        tmpx.append(tmp[0])
        tmpy.append(tmp[1])
    half = len(tmpx) // 2
    medianx = sorted(tmpx)[half]
    mediany = sorted(tmpy)[half]

    #用分布确定范围 离散地取20个点  !!!!以后可以做算法提升的点：如果存在大片空地，则忽略——以实现精准判断
    distancex = max(tmpx) - min(tmpx)
    distancey = max(tmpy) - min(tmpy)
    integral = []
    for d in range(0,20):
        rangex = distancex//d
        rangey = distancey//d
        ans = 0
        for cellular in temp:
            if cellular[0] in (medianx-distancex//(d+1),medianx+distancex//(d+1)) and cellular[1] in (medianx-distancex//(d+1),medianx+distancex//(d+1)):
                ans += 1
        integral.append(ans)
    for i in range(len(integral)):
        if integral[i] >= half*1.7:
            choice = i+1
            break
    idealx = (medianx - (distancex*choice)//20, medianx + (distancex*choice)//20)
    idealy = (mediany - (distancey*choice)//20, mediany + (distancey*choice)//20)
    



def auto_vitalize():
    pass #自动随机生成元胞
"""




def generate():
    global screenx, screeny, world
    next_generation_world = dict()
    for cellular in world:
        x, y = cellular
        search_range = ((x-1,y-1),(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1),(x-1,y))
        count = sum(
            1
            for location in search_range
            if world.__contains__(location) and world[location]
        )
        if count == 3 or (count==2 and world[cellular]):
            next_generation_world[cellular] = True
            for space in search_range:
                if not next_generation_world.__contains__(space):
                    next_generation_world[space] = False
        elif count != 0:
            next_generation_world[cellular] = False

    if world == next_generation_world:
        return True
    world = next_generation_world




def change_color(editing=False):
    global color1, color2, length
    if editing:
        color1 = (0,min(length-1,255),0)
        color2 = (0,255,0)
    else:
        color1 = (min(length-1,255),min(length-1,255),min(length-1,255))
        color2 = (255,255,255)




def update():
    global window
    while True:
        window.fill((0,0,0))
        world_copy = world.copy()
        if length >= 16:
            for x in range(-origin[0],screenx//length-origin[0]+1):
                for y in range(-origin[1],screeny//length-origin[1]+1):
                    pygame.draw.rect(window,color1,((x+origin[0])*length,(y+origin[1])*length,length,length),1)            
        for cellular in world_copy:
            x, y = cellular
            if x in range(-origin[0],screenx//length-origin[0]+1) and y in range(-origin[1],screeny//length-origin[1]+1) and world_copy[(x,y)]:
                pygame.draw.rect(window,color2,((x+origin[0])*length,(y+origin[1])*length,length,length))

        pygame.display.flip()
        clock.tick(60)





def running():
    global screenx, screeny, length, origin, window
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]//length - origin[0]
                y = event.pos[1]//length - origin[1]
                if event.button == 4:
                    if length < min(screenx,screeny)//4:
                        origin[0] -= x
                        origin[0] //= 2
                        origin[1] -= y
                        origin[1] //= 2
                        length *= 2
                    change_color()
                elif event.button == 5:
                    if length > 1:
                        origin[0] += x//2
                        origin[0] *= 2
                        origin[1] += y//2
                        origin[1] *= 2
                        length //= 2
                    change_color()
                elif event.button == 1:
                    change_color(True)
                    while pygame.MOUSEBUTTONUP not in map(lambda x:x.type, pygame.event.get()):
                        x = pygame.mouse.get_pos()[0]//length - origin[0]
                        y = pygame.mouse.get_pos()[1]//length - origin[1]
                        world[(x,y)] = True
                        search_range = ((x-1,y-1),(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1),(x-1,y))
                        for space in search_range:
                            if not world.__contains__(space):
                                world[space] = False
                    change_color()
                elif event.button == 3:
                    world[(x,y)] = False
                elif event.button == 2:
                    change_color(True)
                    return None
                break
            elif event.type == pygame.VIDEORESIZE:
                size = screenx, screeny = event.size
                window = pygame.display.set_mode(size, flags = pygame.RESIZABLE )
                change_color()
                break
            elif event.type == pygame.QUIT:
                quit()

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                change_color(True)
                return None

            pygame.event.clear()

        if generate():
            change_color(True)
            return None







def edit():
    global screenx, screeny, length, origin, window
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]//length - origin[0]
                y = event.pos[1]//length - origin[1]
                if event.button == 4:
                    if length < min(screenx,screeny)//4:
                        origin[0] -= x
                        origin[0] //= 2
                        origin[1] -= y
                        origin[1] //= 2
                        length *= 2
                    change_color(True)
                elif event.button == 5:
                    if length > 1:
                        origin[0] += x//2
                        origin[0] *= 2
                        origin[1] += y//2
                        origin[1] *= 2
                        length //= 2
                    change_color(True)
                elif event.button == 1:
                    while pygame.MOUSEBUTTONUP not in map(lambda x:x.type, pygame.event.get()):
                        x = pygame.mouse.get_pos()[0]//length - origin[0]
                        y = pygame.mouse.get_pos()[1]//length - origin[1]
                        world[(x,y)] = True
                        search_range = ((x-1,y-1),(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1),(x-1,y))
                        for space in search_range:
                            if not world.__contains__(space):
                                world[space] = False
                elif event.button == 3:
                    world[(x,y)] = False
                elif event.button == 2:
                    change_color()
                    running()
                break
            elif event.type == pygame.VIDEORESIZE:
                size = screenx, screeny = event.size
                window = pygame.display.set_mode(size, flags = pygame.RESIZABLE )
                change_color(True)
                break
            elif event.type == pygame.QUIT:
                quit()

            pygame.event.clear()
            
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                change_color()
                running()




#开始
screencaption = pygame.display.set_caption('GAME OF LIFE ---- Cellular Automaton ---- ruled by John Conway')
os.environ['SDL_VIDEO_CENTERED'] = '1'
window = pygame.display.set_mode([screenx,screeny], flags = pygame.RESIZABLE )
change_color(True)
clock = pygame.time.Clock()
_thread.start_new_thread(update, ())
edit()






"""
接下来还可以做的改进：

generate多线程化

更多可调整的参数
存储和读取图形
无级缩放
自动识别图形
支持其他规则
超级Zoom

"""