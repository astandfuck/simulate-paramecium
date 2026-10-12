import core.Environment as E
import random

class Paramecium:
    def __init__(self, environment, p_num = 10):
        self.environment = environment
        self.env = self.environment.env
        self.env_values = self.environment.env_values

        self.p_num = p_num
        self.paramecia = {}

    def __call__(self):
        """
        用于打印各个草履虫的信息
        """
        for i in range(1, len(self.paramecia)+1):
            print(i, ': ', self.paramecia[i])
        print()

    def update_click(self, click_y, click_x):
        """
        在special中传入start函数，用于记录在鼠标点击位生成的草履虫，
        更新在parameciums字典中（记录为最后的编号+1）
        """
        self.paramecia.update({len(self.paramecia)+1 : [(click_y,click_x), None, 0]})

    def generate_paramecium(self):
        """
        在environment.width与environment.height范围中，
        随机挑选env为空（=0）的位置生成草履虫（=9），
        并将位置坐标（y，x）保存在parameciums字典中，
        ！！！ 这里首次创建了parameciums字典对应的键值对，值为 [(y,x), None, 0]
        """
        for num in range(1, self.p_num+1):
            x = random.randint(0, self.environment.width-1)
            y = random.randint(0, self.environment.height-1)
            if self.env[y][x] == 0 :
                self.env[y][x] = 9
                self.paramecia[num] = [(y,x), None, 0]

    def sense_value(self):
        """
        获取周围的env_values环境的值，
        范围是他自身的八个方位，
        这个属性存储在parameciums字典值的第二位
        """
        for num in range(1, len(self.paramecia) + 1):
            y, x = self.paramecia[num][0]
            list_values = []
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if abs(dx) != 0 or abs(dy) != 0:  #防止中心点(0,0)进入循环
                        new_y = y + dy
                        new_x = x + dx
                        if 0 <= new_y < self.environment.height and 0 <= new_x < self.environment.width :
                            list_values.append(self.env_values[new_y][new_x])
            self.paramecia[num][1] = tuple(list_values)

    def move_randomly(self):
        """
        随机向草履虫的8个方向中的一个移动，
        吃掉落点位置的食物（草履虫的第三个属性加1）
        原位变为空
        """
        for num in range(1, len(self.paramecia) + 1):
            y, x = self.paramecia[num][0]
            new_y = y + random.choice([-1, 0, 1])
            new_x = x + random.choice([-1, 0, 1])
            if new_y == y and new_x == x:
                continue
            if 0 <= new_x < self.environment.width and 0 <= new_y < self.environment.height :
                if self.env[new_y][new_x] == 1 :  #新位置是食物
                    self.env[new_y][new_x] = 9  #新位置变为草履虫
                    self.env[y][x] = 2  #旧位置变为空
                    self.paramecia[num][0] = (new_y, new_x)  #草履虫的位置记录改变
                    self.paramecia[num][2] += 1 #记录吃到的食物数加1
                else:
                    self.env[new_y][new_x] = 9
                    self.env[y][x] = 2
                    self.paramecia[num][0] = (new_y, new_x)


if __name__ == '__main__':

    def main():
        environment = E.Environment()
        paramecium = Paramecium(environment, p_num=10)

        def setup(_environment: E.Environment):
            environment.generate_food()
            paramecium.generate_paramecium()

        def loop(_environment: E.Environment):
            environment.spread()
            paramecium.move_randomly()
            paramecium.sense_value()
            paramecium()

        def special(click_y, click_x):
            paramecium.update_click(click_y, click_x)

        E.start(environment, setup, loop, special, fps=60)

    main()