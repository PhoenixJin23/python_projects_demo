class Settings:#把所有设置放到Settings这个类里面
    """存储《外星人入侵》游戏所有可配置参数的类，统一管理屏幕、飞船、子弹等设置"""
    def __init__(self):
        # settings.py 配置文件，集中管理所有固定参数
        self.aliens_point = None
        self.SCREEN_WIDTH = 1200  # 屏幕宽度
        self.SCREEN_HEIGHT = 800  # 屏幕高度
        # 开始搞怪
        self.SCREEN_CAPTION = "Gradient Background"  # 窗口标题
        # 渐变颜色配置（起始色：橙色，结束色：粉色）
        self.GRADIENT_START_COLOR = (255, 153, 102)  # 橙色 RGB
        self.GRADIENT_MID_COLOR = (255, 255, 255)  # 中间色：白色
        self.GRADIENT_END_COLOR = (255, 179, 217)  # 粉色 RGB
        self.bg_surface = None

        self.ship_speed=0.5#使得ship每次更新时移动长度可以发生变化
        self.bullet_speed = 0.25  # 子弹速度，数值越大越快
        self.bullet_width = 5  # 子弹宽度（像素），3是比较合适的数值
        self.bullet_height=8
        self.bullet_color = (60, 60, 60)  # 子弹颜色（深灰色）
        self.bullets_allowed=10
        self.alien_speed=0.3
        self.fleet_drop_speed=1
        self.fleet_direction=1#1为向右，-1为向左
        #记录外星人移动左右方向，不用布尔值是因为数字还可以表示移动的距离
        self.ship_limit=3#玩家初始拥有飞船数量
        #加快游戏节奏
        self.speedup_scale=1.1
        #外星人分数的提高速度
        self.score_scale=1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed=0.5
        self.bullet_speed=0.5
        self.alien_speed=0.3
        #fleet_direction为1表示向右，-1为向左
        self.fleet_direction=1
        #计分
        self.alien_point=50

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        self.alien_point=int(self.score_scale*self.alien_point)
