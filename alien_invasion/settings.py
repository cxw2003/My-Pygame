class Settings:
    """存储游戏中设置的类"""
    def __init__(self):
        """初始化游戏设置"""
        #屏幕设置
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(115,116,123)
        #飞船设置
        self.ship_speed =2.0
        self.ship_limit=3
        #子弹设置
        self.bullet_speed=2.0
        self.bullet_width=50
        self.bullet_height=50
        self.bullet_color=(197,200,201)
        self.bullets_allowed=10
        #外星人设置
        self.alien_speed=1.0
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，为-1表示向左移。
        self.fleet_direction = 1
