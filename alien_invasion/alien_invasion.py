#导入模块sys,pygame
import sys
from time import sleep

import pygame

from settings import Settings

from game_stats import GameStats

from button import Button

from ship import Ship

from bullet import Bullet

from alien import Alien

class AlienInvasion:
	"""管理游戏资源和行为的类"""
	def __init__(self):
		"""初始化游戏并创建游戏资源"""
		pygame.init()	# 初始化pygame模块
		self.settings=Settings()	#创建Settings实例并关联
		self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))	#创建一个显示窗口
		self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.settings.screen_width=self.screen.get_rect().width	#更新设置
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Only my railgun")	#设置窗口上的标题
		#创建一个用于存储游戏统计信息的实例
		self.stats=GameStats(self)
		self.ship=Ship(self)
		self.bullets=pygame.sprite.Group()	#创建子弹编组（类似于列表）
		self.aliens=pygame.sprite.Group()
		self._create_fleet()
		#创建play按钮
		self.play_button=Button(self,"Play")

	def run_game(self):
		"""开始游戏的主循环"""
		while True:
			self._check_events()	#检测按键鼠标
			if self.stats.game_active:
				self.ship.update()	#更新飞船位置
				self._update_bullets()
				self._update_aliens()
			self._update_screen()

	def _check_events(self):
		"""响应按键和鼠标事件"""
		for event in pygame.event.get():  # 事件循环，监视键盘和鼠标,访问事件列表
			if event.type == pygame.QUIT:  # ???
				sys.exit()
			elif event.type==pygame.KEYDOWN:	#检测类型（按下或松开）和按键（上下左右）
				self._check_keydown_events(event)
			elif event.type==pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type==pygame.MOUSEBUTTONDOWN:
				mouse_pos =pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self,mouse_pos):
		"""在玩家单击Play按钮时开始新游戏"""
		button_clicked=self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#重置游戏统计信息
			self.stats.reset_stats()
			self.stats.game_active =True

			#清空余下的外星人和子弹
			self.aliens.empty()
			self.bullets.empty()

			#创建一群新的外星人并让飞船居中
			self._create_fleet()
			self.ship.center_ship()

			#隐藏鼠标光标
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self,event):
		"""响应按键"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True  # 不直接修改图片位置，而是更改状态值，允许持续移动
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key==pygame.K_q:
			sys.exit()
		elif event.key==pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self,event):
		"""响应松开"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""创建一颗子弹，并将其加入编组bullets中"""
		if len(self.bullets)<self.settings.bullets_allowed:	#限制子弹数量
			new_bullet=Bullet(self)	#new add为pygame专属
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""更新子弹的位置并删除消失的子弹"""
		#更新子弹的位置
		self.bullets.update()  # 精灵自动遍历编组使用update
		# 删除消失的子弹
		for bullet in self.bullets.copy():  # pygame编组列表长度要求不变，所以必须遍历编组的副本
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		# print(len(self.bullets))	#终端调试
		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		"""响应子弹和外星人的碰撞"""
		#删除发生碰撞的子弹和外星人。

		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)
		if not self.aliens:
			# 删除现有的子弹并新建一群外星人。
			self.bullets.empty()
			self._create_fleet()

	def _update_aliens(self):
		"""
		检查是否有外星人位于屏幕边缘
		并更新外星人群中所有外星人的位置
		"""
		self._check_fleet_edges()
		self.aliens.update()
		#检测外星人和飞船之间的碰撞。
		if pygame.sprite.spritecollideany(self.ship,self.aliens):
			self._ship_hit()
		#检查是否有外星人到达了屏幕底端
		self._check_aliens_bottom()


	def _create_fleet(self):
		"""创建外星人群"""
		#创建一个外星人并计算一行可容纳多少个外星人
		#外星人的间距为外星人宽度
		alien=Alien(self)	#创建实例
		alien_width,alien_height =alien.rect.size
		available_space_x = self.settings.screen_width-(2*alien_width)
		number_aliens_x = available_space_x //(2*alien_width)+1

		#计算屏幕可容纳多少行外星人。
		ship_height=self.ship.rect.height
		available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height)
		number_rows=available_space_y//(2*alien_height)

		#创建外星人群
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number,row_number)

	def _create_alien(self,alien_number,row_number):
			#创建一个外星人并将其加入当前行
			alien = Alien(self)
			alien_width,alien_height =alien.rect.size
			alien.x = alien_width+2*alien_width*alien_number
			alien.rect.x = alien.x
			alien.rect.y=2*(alien.rect.height-30)*row_number
			self.aliens.add(alien)	#加入到编组

	def _check_fleet_edges(self):
		"""有外星人到达边缘时采取相应的措施。"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""将整群外星人下移，并改变它们的方向。"""
		for alien in self.aliens.sprites():
			alien.rect.y+=self.settings.fleet_drop_speed
		self.settings.fleet_direction *=-1

	def _ship_hit(self):
		"""响应飞船被外星人撞到"""
		if self.stats.ships_left>=0:
			#将ships_left减1
			self.stats.ships_left-=1
			#清除余下的外星人和子弹
			self.aliens.empty()
			self.bullets.empty()
			#创建一群新的外星人，并将飞船放到屏幕底端的中部
			self._create_fleet()
			self.ship.center_ship()
			#暂停
			sleep(0.5)
		else:
			self.stats.game_active=False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		"""检查是否有外星人到达了屏幕底端"""
		screen_rect =self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom>=screen_rect.bottom:
				#像飞船被撞一样处理
				self._ship_hit()
				break

	def _update_screen(self):
		"""更新屏幕上的图像，并切换到新屏幕"""
		self.screen.fill(self.settings.bg_color)  # 每次循环时都重绘屏幕
		self.ship.blitme()
		for bullet in self.bullets.sprites():	#遍历精灵（元素）
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		#如果游戏处于非活动状态，就绘制Play按钮
		if not self.stats.game_active:
			self.play_button.draw_button()
		pygame.display.flip()  # 屏幕刷新

if __name__=='__main__':	#模拟程序入口
	ai=AlienInvasion()		#创建游戏实例并运行游戏
	ai.run_game()			#设置简短或易记的名，有效避免出错

