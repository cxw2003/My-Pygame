import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):   #使用精灵sprite,将游戏中相关的元素编组，进而同时操作编组中的所有元素
    """管理飞船发射子弹的类"""

    def __init__(self,ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()  #继承
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        # self.image = pygame.image.load('images/lightning.png')
        # self.rect = self.image.get_rect()
        self.color=self.settings.bullet_color
        # #在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)   #并非图像，从头创建
        self.radius=10
        self.width=10
        self.rect.midtop=ai_game.ship.rect.midtop
        #存储用小数表示的子弹位置（便于微调）
        self.y=float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        #更新表示子弹位置的小数值
        self.y-=self.settings.bullet_speed
        #更新表示子弹的rect的位置
        self.rect.y=self.y

    # def draw_bullet(self):
    #     """在指定位置绘制飞船"""
    #     self.screen.blit(self.image, self.rect)

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
