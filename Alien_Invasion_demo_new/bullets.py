import pygame
from pygame.sprite import Sprite
#Sprite模块能把多个游戏元素进行编组，方便统一操作（子弹有很多个）


class Bullet(Sprite):
    """管理飞船所发射子弹的类"""

    def __init__(self,ai_game):
        """在飞船当前位置创建一个子弹对象，依赖游戏实例（ai_game）获取屏幕、配置等资源"""
        super().__init__()#子弹的父类是Sprite，用__init__方法把父类相关的属性初始化

        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color

        #在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop#子弹一开始在飞船的正上方

        #储存用小数表示的子弹位置
        self.y=float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        #更新表示子弹位置的小数值
        self.y-=self.settings.bullet_speed
        #纵坐标等于当前纵坐标-子弹速度，相当于把子弹往上移动

        #更新表示子弹的rect的位置
        self.rect.y=self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)
        #子弹的位置尺寸等信息都是通过rect这个变量记录的

