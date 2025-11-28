import pygame#引入pygame，操作飞船也需要相关的功能
from pygame.sprite import Sprite

class Ship(Sprite):#Sprite更方便对编组进行管理
    """"管理飞船的类"""

    def __init__(self, ai_game):
        #给类几个属性，包括screen，赋值为传入的外星人入侵游戏的窗口
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen=ai_game.screen#方便直接通过属性（screen）直接对游戏窗口（ai_game)操作
        self.screen_rect=ai_game.screen.get_rect()
        #screen_rect赋值为游戏窗口的句型，这个属性帮助定位游戏里不同元素的位置

        #加载飞船图并获取其外接矩形
        self.image = pygame.image.load("images/ship.png").convert_alpha()#让image等于文件加载出来的图片对象
        self.rect=self.image.get_rect()#rect让它为飞船图像的外接矩形
        self.settings=ai_game.settings#新建一个属性，让它等于这个游戏的settings
        # 游戏的settings相当于self.settings=Settings()构造函数里的变量

        #对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom=self.screen_rect.midbottom
        #让飞船图像外界矩形底部中央的位置等于游戏窗口底部中央的位置，相当于把飞船放在游戏窗口底部中央的位置
        self.x=float(self.rect.x)#原始self.x只能储存整数，所以用额外的x储存真正的浮点数
        self.moving_right=False#什么时候正在移动的属性为True呢？
        self.moving_left=False

    def blitme(self):
    #调用该方法时，会在传入的外星人入侵游戏窗口里，把飞船图像画在对应的位置
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)#已经让self.rect的位置与游戏窗口底部中央对齐了
    #了解pygame坐标位置逻辑：左上角为（0，0），横为x，纵为y

    def update(self):
        """"根据移动标志调整飞船的位置，限制在屏幕边界内"""
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x+=self.settings.ship_speed#每次x增减值是和速度对应
        if self.moving_left and self.rect.left>0:
            self.x-=self.settings.ship_speed
            #在x上进行加减，因为rect.x只能储存整数，x储存的是真正浮点数的值
        self.rect.x=self.x

    def center_ship(self):
        """让飞船在屏幕底部居中"""
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)

