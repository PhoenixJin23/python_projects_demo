import pygame
import sys
from time import sleep#帮助暂停游戏
from settings import Settings#文件名 import 类名
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard



class AlienInvasion:
    """管理游戏资源和循环的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()#初始化游戏，必不可少#游戏初始化时需要构造实例
        self.settings=Settings()#类是 “抽象模板”，实例是 “具体实物”，实例化就是把模板变成实物的过程
        #为了能访问Settings类里的资源，设置一个新的属性settings并把它赋值给类的一个实例
        #通过创建Settings类的实例（这个实例包含了所有游戏配置），把游戏的所有配置 “打包” 到self.settings里
        #settings 是 AlienInvasion 类的实例属性，这个属性的值是Settings类的一个实例
        #AlienInvasion 类通过自己的 settings 属性，持有了一个 Settings 类的实例。
        #这个类的作用是储存固定的游戏配置（比如屏幕宽高、子弹速度），它不需要依赖 “当前游戏的状态”（比如飞船位置、屏幕对象）所以不用(self)
        self.screen=pygame.display.set_mode((self.settings.SCREEN_WIDTH,self.settings.SCREEN_HEIGHT))
        #给类创建一个screen属性，返回一个游戏的展示屏幕，传入的元组可设置窗口的宽和高（单位：像素）
        #让尺寸数据从属性里获取
        pygame.display.set_caption("Alien Invasion")#设置游戏的名字
        #self.bg_color=(138,206,0) #设置背景色：红，绿，蓝，最多255
        # 预生成渐变背景
        self._create_gradient_background()
        #创建储存游戏统计信息的实例，并创建记分牌
        self.stats=GameStats(self)
        self.scoreboard=Scoreboard(self)
        # 创建一个用于储存游戏统计数据信息的实例
        self.stats=GameStats(self)
        self.ship=Ship(self)#创建新属性，把它赋值为飞船的一个实例
        #飞船的构造函数还需要一个游戏实例，所以把当前游戏传进去。当飞船拿到游戏实例后，就将自己绘制到游戏屏幕上
        #需要传入的参数有两个，self代表AlienInvasion本身，作为实参传入ai_game，帮助ship访问AlienInvasion
        #飞船需要依赖当前游戏的资源才能正常工作,所以有(self)
        self.bullets=pygame.sprite.Group()#创建一个子弹的编组
        self.aliens=pygame.sprite.Group()#创建，把空的编组先赋值给aliens属性
        self._create_fleet()  # 调用方法
        #创建Play按钮
        self.play_button=Button(self,"Play")#把按钮作为游戏的属性


    def run_game(self):#游戏是由run_game这个方法控制的，一旦被调用游戏就会开始运行
        while True:#只要游戏不被手动中断，程序会一直运行，每次循环都会运行以下代码
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            #先更新游戏元素的位置，再刷新屏幕
            self._update_screen()


    def _check_events(self):#以下划线开头的方法，有私密性，只能在当前的类使用
        # 监视鼠标和键盘事件
        for event in pygame.event.get():  # pygame.event.get()会返回一切用户事件
            # 每次循环可能同时发生很多事情，用for循环迭代每件事
            if event.type == pygame.QUIT:
                sys.exit()  # 只要事件是退出（用户点窗口的×），就停止程序运行
            elif event.type==pygame.KEYDOWN:#事件类型如果是按下键盘按键
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()#返回包含点击位置的坐标的元组
                self._check_play_button(mouse_pos)


    def _check_play_button(self,mouse_pos):
        """玩家单击Play按钮时开始游戏"""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #重置游戏设置
            self.settings.initialize_dynamic_settings()
            #重置游戏统计数据
            self.stats.reset_stats()
            self.stats.game_active=True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()
            #隐藏鼠标光标
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self,event):#只处理按下键盘的方法
        """响应键盘"""
        if event.key == pygame.K_RIGHT:  # 并且按下的键是右键
            # self.ship.rect.x+=1  就把飞船的外接矩形向右移动————这个只能实现单次按右键移动，不能长按右键连续移动
            self.ship.moving_right = True  # 按下右键，moving_right属性为真
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self,event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False  # 松开右键，moving_right属性为假
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _update_screen(self):
        # 绘制预生成的渐变背景
        self.screen.blit(self.settings.bg_surface, (0, 0))
        # 绘制飞船、子弹、外星人
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #显示得分
        self.scoreboard.show_score()
        #如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
        # 刷新屏幕
        pygame.display.flip()


    def _create_gradient_background(self):
        """预生成渐变背景，只绘制一次"""
        self.settings.bg_surface = pygame.Surface(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        # 贴近 Lesbian Flag 的橙粉配色（更柔和且贴合旗帜基调）
        start_color = (255, 140, 110)  # 旗帜感深橙
        mid_color = (255, 255, 255)  # 白色窄条
        end_color = (200, 100, 180)  # 旗帜感深粉

        H = self.settings.SCREEN_HEIGHT  # 固定 800 像素高度，避免计算误差
        # 明确分段（覆盖整个窗口，无遗漏）
        orange_to_white_end = 320  # 橙→白：0~320 像素（占 40%）
        white_to_pink_end = 800  # 白→粉：480~800 像素（占 40%）
        white_start = 320  # 白色开始：320 像素
        white_end = 480  # 白色结束：480 像素（占 20%，窄条）

        # 1. 深橙 → 白色（0 ~ 320 像素）
        s_r, s_g, s_b = start_color
        m_r, m_g, m_b = mid_color
        for y in range(0, orange_to_white_end):
            ratio = y / orange_to_white_end
            r = int(s_r + (m_r - s_r) * ratio)
            g = int(s_g + (m_g - s_g) * ratio)
            b = int(s_b + (m_b - s_b) * ratio)
            pygame.draw.line(self.settings.bg_surface, (r, g, b), (0, y), (self.settings.SCREEN_WIDTH, y))

        # 2. 纯白色窄条（320 ~ 480 像素）
        for y in range(white_start, white_end):
            pygame.draw.line(self.settings.bg_surface, mid_color, (0, y), (self.settings.SCREEN_WIDTH, y))

        # 3. 白色 → 深粉（480 ~ 800 像素，全覆盖底部）
        e_r, e_g, e_b = end_color
        for y in range(white_end, H):
            ratio = (y - white_end) / (H - white_end)
            r = int(m_r + (e_r - m_r) * ratio)
            g = int(m_g + (e_g - m_g) * ratio)
            b = int(m_b + (e_b - m_b) * ratio)
            pygame.draw.line(self.settings.bg_surface, (r, g, b), (0, y), (self.settings.SCREEN_WIDTH, y))


    def _update_bullets(self):
        self.bullets.update()#每次循环都更新子弹编组，组里每一个子弹的update方法都被执行了
        for bullet in self.bullets.copy():  # 遍历编组里的每个子弹
            # 遍历编组复制后的副本，因为python的for循环不允许迭代过程中迭代对象的长度改变，否则会遗漏或重复操作
            if bullet.rect.bottom <= 0:  # 当子弹飞出屏幕外面
                self.bullets.remove(bullet)  # 就把飞出去的子弹从编组里移除出去，子弹越来越多影响程序的运行
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞，并在所有外星人全部死亡后生成新的外星人群"""
        # 检测是否有子弹击中了外星人，如果有，就删除子弹和外星人
        collisions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True)
        if collisions:
            print(f"碰撞发生！当前分数: {self.stats.score}")
            # 累加得分（多个外星人被击中时不遗漏）
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_point*len(aliens)
                self.scoreboard.prep_score()#重新绘制分数信息
                self.scoreboard.check_high_score()
        if not self.aliens:
            #删除现有的子弹并新建一群外星人,并加速
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #提高等级
            self.stats.level+=1
            self.scoreboard.prep_level()


    def _fire_bullet(self):
        """创建一个子弹并将其加入bullets编组里"""
        """限制发射子弹的数量"""
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)


    def _create_fleet(self):
        """创建外星人群"""
        #创建一个外星人并计算一行可容纳多少个外星人
        alien=Alien(self)
        # 2. 计算横向可容纳的外星人数（左右各留1个外星人宽度的边距）
        alien_width=alien.rect.width
        available_space_x = self.settings.SCREEN_WIDTH - (2 * alien_width)
        # 每个外星人占2个宽度（自身宽度 + 1个宽度的间距），向下取整确保不超出屏幕
        number_aliens_x = available_space_x // (2 * alien_width)
        alien_height=alien.rect.height
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.SCREEN_HEIGHT-(3*alien_height)-ship_height)
        number_rows=available_space_y//(2*alien_height)

        #创建第一行外星人
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)


    def _create_alien(self,alien_number,row_number):
        # 创建一个外星人并将其加入当前行
        alien = Alien(self)
        alien_width=alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number  # 新的外星人要依次向右推移2个外星人的宽度（间隔1个外星人宽度）
        alien.rect.x = alien.x
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)


    def _update_aliens(self):
        """更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()#先check和调整外星人竖向位置，再更新横向位置
        self.aliens.update()#对aliens编组调用update方法，使编组中每个外星人都去执行update方法
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
        #spritecollideany()方法接收两个参数，一个是pygame游戏元素，一个是pygame游戏的编组
        #用来检查第一个参数的元素有没有和第二个参数的编组中的任何一个成员发生碰撞，若有，返回True
            #print("Ship hit!!!")#占个位先
            self._ship_hit()#如果飞船发生了碰撞
            self._check_aliens_bottom()#或者外星人到达了底部，都让ship_left属性-1


    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1


    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        #将 ships_left 减1
        if self.stats.ship_left>0:
            self.stats.ship_left-=1
            self.scoreboard.prep_ships()

            #清除余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else:
            self.stats.game_active=False
            #此处包含游戏结束相关的逻辑，添加游戏结束时光标恢复的相关代码
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                #像飞船被撞到一样处理
                self._ship_hit()
                break



if __name__=='__main__':
    #创建游戏实例并运行游戏
    ai=AlienInvasion()
    ai.run_game()
    #如果运行的主程序是当前该文件，新建一个Alien Invasion游戏，并调用run_game方法，即开始游戏的主循环
