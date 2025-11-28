import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""
    #Sprite类方便对编组进行管理，外星人很多，需要批量管理

    def __init__(self,ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()#调用父类的构造函数
        self.screen=ai_game.screen#将游戏屏幕设置为screen属性，方便后续调用
        self.settings=ai_game.settings#先获得游戏的设置类，才能获得速度的信息
        #加载外星人图像并设置其rect属性
        self.image=pygame.image.load('images/alien.png').convert_alpha()
        self.rect=self.image.get_rect()


        #每个外星人最初都在屏幕的左上角附近
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        #离左上角（0，0）有外星人外界矩形的宽高距离

        #储存外星人的精确水平位置
        self.x=float(self.rect.x)


    def update(self):
        """向右移动外星人"""
        #self.x+=self.settings.alien_speed#先更新更精准的浮点位置
        self.x+=self.settings.alien_speed*self.settings.fleet_direction
        #加强版，路程=速度*循环次数*方向（+1/-1）
        self.rect.x=self.x#再让外星人的位置等于这个浮点位置


    def check_edges(self):
        """如果外星人在屏幕边缘，就返回True"""
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right or self.rect.left<=0:
            return True


