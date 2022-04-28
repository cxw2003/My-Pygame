import pygame

class Ship:
    """管理飞船的类"""

    def __init__(self,ai_game): #ai_game是指向当前Alien Invasion实例的引用
        """初始化飞船并设置其初始位置。"""    #这使Ship可以访问Alien Invasion中定义的所有游戏资源
        self.screen =ai_game.screen
        self.settings =ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()  #rect对象，矩形，方便检测碰撞

        #加载飞船图像并获取其外接矩形。
        self.image=pygame.image.load('images/railgun1.png')
        self.rect=self.image.get_rect()

        #对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom=self.screen_rect.midbottom

        #在飞船的属性x中存储小数值
        self.x=float(self.rect.x)

        #移动标志
        self.moving_right=False
        self.moving_left=False

    def update(self):
        """根据移动标志调整飞船位置"""
        #更新飞船而不是rect对象的X值
        if self.moving_right and self.rect.right<self.screen_rect.right:    #and后条件测试，限制飞船活动范围
            self.x +=self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x -=self.settings.ship_speed
        #根据self.x更新rect对象
        self.rect.x=self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """让飞船在屏幕底部居中"""
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)