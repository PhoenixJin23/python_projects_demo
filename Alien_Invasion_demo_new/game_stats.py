class GameStats:
    """跟踪游戏的统计信息"""
    #想通过数据记录发生碰撞的次数，方便统计得分

    def __init__(self,ai_game):
        """初始化统计信息"""
        self.settings=ai_game.settings
        self.reset_stats()
        #游戏刚启动时出于非活动状态
        self.game_active=False
        #任何情况下都不应该重置最高得分
        self.high_score=0

    def reset_stats(self):#用来重置信息的方法
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ship_left=self.settings.ship_limit
        #将游戏剩余的飞船数量恢复成初始值，有利于每次开局重设游戏数据
        self.score=0
        self.level=1