import pygame.font
from pygame.sprite import Sprite
from ship import Ship
from pygame.sprite import Group


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self,ai_game): #ai_game接收到AlienInvasion对象
        #灵活性高：记分牌可以访问游戏的任何部分，面向对象
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game #保存这个引用(整个游戏)，由ai_game连接了AlienInvasion的多个部件
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.settings=ai_game.settings
        #显示得分信息时使用的字体设置
        self.text_color=(255, 255, 255)
        self.font=pygame.font.SysFont(None,48)
        #准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        # 关键修改：每次都从ai_game获取最新的stats
        score = self.ai_game.stats.score  #通过游戏对象直接访问最新的分数
        rounded_score = round(score, -1) #round表示取整，-1表示向小数点前1位取整，aka取10的整倍数
        score_str="{:,}".format(rounded_score) #字符串格式化，:,给数字添加千位分隔符
        self.score_image=self.font.render(score_str,True,self.text_color,None)
        #在屏幕右上角显示得分
        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20 #距离屏幕最右侧20像素的位置
        self.score_rect.top=20 #距离顶端也是20像素的距离
        print(f"更新记分牌，真实分数: {score}")


    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        #使用 ai_game.stats 获取最新数据
        high_score=round(self.ai_game.stats.high_score,-1)
        high_score_str="{:,}".format(high_score)
        self.high_score_image=self.font.render(high_score_str,True,self.text_color,None)

        #将最高得分放在屏幕顶部中央
        self.high_score_rect=self.high_score_image.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx
        self.high_score_rect.top=self.score_rect.top
        print(f"最高分: {self.ai_game.stats.high_score}")


    def prep_level(self):
        """将等级转换为渲染的图像"""
        level_str=str(self.ai_game.stats.level)
        self.level_image=self.font.render(level_str,True,self.text_color,None)

        #将等级放在得分下面
        self.level_rect=self.level_image.get_rect()
        self.level_rect.right=self.score_rect.right
        self.level_rect.top=self.score_rect.bottom+10
        print(f"等级：{self.ai_game.stats.level}")


    def prep_ships(self):
        """显示还剩余多少飞船"""
        self.ships=Group() #添加一个编组
        for ship_number in range(self.ai_game.stats.ship_left):
            ship=Ship(self.ai_game)
            ship.rect.x=10+ship_number*ship.rect.width #位置：每艘船距离顶部10像素
            ship.rect.y=10
            self.ships.add(ship) #剩几艘船就把几艘船添加到编组里面


    def show_score(self):
        #在游戏上显示得分
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)


    def check_high_score(self):
        #检查是否诞生了新的最高分
        if self.ai_game.stats.score>self.ai_game.stats.high_score:
            self.ai_game.stats.high_score=self.ai_game.stats.score
            self.prep_high_score()
