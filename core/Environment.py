#%%
import sys 
import pygame 
import random
#%%
#窗口大小和比例SCALE
# WIDTH = 250
# HEIGHT = 250
SCALE = 3

#颜色
COLOR_EMPTY = (0, 0, 0)
COLOR_VALUES = (0 , 0, 255)
COLOR_FOOD = (0, 255, 0)
COLOR_OBSTACLE = (50, 50, 50)
COLOR_PARAMECIUM = (255, 0, 0)

# 草履虫感知范围
SENSE_RADIUS = 10
GENERATE_RADIUS = 20

#食物、障碍生成速率
FOOD_RATE = 0
OBSTACLE_RATE = 0

paramecium_dic = {}
food_click_list = []
add_delay = 0
last_add_time = 0.0
recursion_num = 0
#%%
class Environment:
    """
    env和env_values的宽高一致，x代表横轴（正方向向右），y代表纵轴（正方向向下），（0，0）点在最左上角
    env的值含义：
    1：食物
    2：障碍物
    3：草履虫
    """
    def __init__(self, food_num:int = 10, max_values:float = 1000.0, _env:list = None, _env_values:list = None, width:int = 250, height:int = 250):
        """
        env和self.env的地址一样，所以操作self.env也会同样改变env
        """
        if _env_values is None:
            self.env_values = [[0 for _ in range(width)]for _ in range(height)]
        else:
            self.env_values = _env_values

        if _env is None:
            self.env = [[0 for _ in range(width)]for _ in range(height)]
        else:
            self.env = _env

        self.width = width
        self.height = height
        self.food_num = food_num
        self.max_values = max_values
        self.food_position = []

    def draw_environment(self, _screen):
        """
        将环境用pygame画出来，类似于涂色
        """
        for y in range(self.height):
            for x in range(self.width):
                # 根据格子值选择颜色
                if self.env[y][x] == 1:
                    color = COLOR_FOOD
                elif self.env[y][x] == 2:
                    color = COLOR_OBSTACLE
                elif self.env[y][x] == 9:
                    color = COLOR_PARAMECIUM
                else:
                    color = COLOR_EMPTY
                pygame.draw.rect(_screen,color,(x * SCALE, y * SCALE, SCALE - 1, SCALE - 1))

    def draw_values(self, _screen):
        """
        将环境中的化学信息画出来
        """
        for y in range(self.height):
            for x in range(self.width):
                # 根据值的比例选择颜色
                relative_size = 255*self.env_values[y][x]/self.max_values
                color = (0, 0, relative_size)
                pygame.draw.rect(_screen,color,(x * SCALE, y * SCALE, SCALE - 1, SCALE - 1))

    def env_values_9_9(self,core_spot:tuple):
        """
        计算以食物点为中心的9*9的数值均值，即溶液末状态,并赋值给env_values(食物点保持原值)
        """
        sum_values = 0.0
        y,x = core_spot
        for i in range(-1,2) :            #-1,0,1(y)
            for j in range(-1,2) :         #-1,0,1(x)
                if 0<=x+j<self.width and 0<=y+i<self.height :
                    sum_values+= self.env_values[y+i][x+j]
        end_values = sum_values/9
        for i in range(-1,2) :
            for j in range(-1,2) :
                if 0<=x+j<self.width and 0<=y+i<self.height :#!!!!!can be promoted
                    if self.env[y+i][x+j] == 0 :
                        self.env_values[y+i][x+j] = end_values

    def spread(self, radius:int = 20)->None:
        """
        radius是各个食物点传播化学信息的矩形范围半径，以radius范围传播化学信息，更改self._env_values的值（call env_values_9_9）
        """
        for food_spot in self.food_position :
            self.env_values_9_9(food_spot)
            y,x = food_spot
            for r in range(1, radius+1):
                for dx_ in range(-r, r+1):
                    for dy_ in range(-r, r+1):
                        if abs(dx_) == r or abs(dy_) == r:
                            cx = x+dx_
                            cy = y+dy_
                            if 0 <= cx < self.width and 0 <= cy < self.height :
                                if self.env[cy][cx] == 0 or self.env[cy][cx] == 1:  #只将食物和空格的坐标传入9_9扩散器！！！！！！！！！
                                    self.env_values_9_9((cy, cx))

    def generate_food(self):
        """
        生成食物并在env上赋值，并记录食物的tuple位置于position
        """
        for _ in range(self.food_num):
            while True :
                x=random.randint(0,self.width-1)
                y=random.randint(0,self.height-1)
                if self.env[y][x] == 0 :
                    self.env[y][x] = 1
                    self.env_values[y][x] = self.max_values
                    self.food_position.append((y,x))
                    break

    def update_values(self):
        """
        更新,由env中新添加的食物,所提供的化学信息env_values
        """
        for row in range(self.height):
            for col in range(self.width):
                if self.env[row][col] == 1:
                    self.env_values[row][col] = self.max_values
                    self.food_position.append((row,col))
#%%
def start(_environment: Environment, _set_up, _loop, _special, fps = 10):

    last_add_time = 0.0

    pygame.init()
    screen = pygame.display.set_mode((_environment.width * SCALE, _environment.height * SCALE))
    pygame.display.set_caption("simulate paramecium")
    clock = pygame.time.Clock()

    running = True
    draw_1 = True
    pygame.key.set_repeat(200,50)

    _set_up(_environment)

    while running :
        current_time = pygame.time.get_ticks()
        clock.tick(fps)#帧数
        keys = pygame.key.get_pressed()
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False

            if event.type == pygame.KEYDOWN :#
                if event.key == pygame.K_q :
                    if draw_1 is True :
                        draw_1 = False
                    else :
                        draw_1 = True
            # if event.type == pygame.MOUSEBUTTONDOWN :
            #     click_x,click_y = event.pos
            #     food_click_list.append((click_x,click_y))
        if keys[pygame.K_ESCAPE] :
            running = False

        #------------------------------------^^---此上为基本的运行设置，有按键作用、帧数等

        left_pressed = pygame.mouse.get_pressed()[0]
        right_pressed = pygame.mouse.get_pressed()[2]
        if left_pressed and current_time - last_add_time > add_delay :#左键长按生产单个食物
            press_x,press_y = pygame.mouse.get_pos()
            food_click_list.append((press_x,press_y))
            last_add_time = current_time
        if right_pressed : #右键长按生产大量的矩阵形状食物
            press_x,press_y = pygame.mouse.get_pos()
            for dx in range(-GENERATE_RADIUS,GENERATE_RADIUS+1):
                for dy in range(-GENERATE_RADIUS,GENERATE_RADIUS+1):
                    new_x = press_x//SCALE + dx
                    new_y = press_y//SCALE + dy
                    if new_y >= 0 and new_x < _environment.width and new_x >= 0 and new_y < _environment.height :
                        if _environment.env[new_y][new_x] != 9 :
                            _environment.env[new_y][new_x] = 1
        if food_click_list :#生成点击的食物点
            for click_x_y in food_click_list:
                click_x,click_y = click_x_y
                click_x = click_x//SCALE
                click_y = click_y//SCALE
                # print(click_x,click_y)
                if click_y >= 0 and click_x < _environment.width and click_x >= 0 and click_y < _environment.height :
                    if _environment.env[click_y][click_x] == 0 or _environment.env[click_y][click_x] == 2:
                        switch = 2
                        if switch == 1:
                            _environment.env[click_y][click_x] = 1  #此处可以决定生成食物
                            _environment.update_values()
                        elif switch == 2:
                            _environment.env[click_y][click_x] = 9  #此处可以决定生成草履虫
                            _special(click_y, click_x)

        food_click_list.clear()

        _loop(_environment)

        # screen.fill(COLOR_EMPTY)
        if draw_1 :
            _environment.draw_environment(screen)
        else :
            _environment.draw_values(screen)
        pygame.display.update()

    pygame.quit()
    sys.exit()
#%%
def setup(_environment: Environment):
    _environment.generate_food()
#%%
def loop(_environment: Environment):
    _environment.spread()
#%%
def main():
    environment = Environment()
    start(environment, setup, loop)
#%%
if __name__ == "__main__":
    main()