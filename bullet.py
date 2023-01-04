import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
	def __init__(self, ai_game):
		"""Klasa przeznaczona do zarządania pociskami wystrzeliwanymi przez statek."""
		super().__init__()
		self.screen = ai_game.screen
		self.setting = ai_game.settings
		self.color = self.setting.bullet_color

		# Utworzenie prostokąta pocisku w punkcie (0, 0), a następnie zdefiniowanie dla niego odpowiedniego położenia.
		self.rect = pygame.Rect(0, 0, self.setting.bullet_width, self.setting.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		# Położenie pocisku jest zdefiniowane za pomocą wartości zmiennoprzecinkowej
		self.y = float(self.rect.y)

	def update(self):
		"""Poruszanie pociskiem po ekranie"""
		# 		Uaktualnienie położenia pocisku
		self.y -= self.setting.bullet_speed
		# 		Uaktualnienie położenia prostokąta
		self.rect.y = self.y

	def draw_bullet(self):
		"""Wyświetlanie pocisku na ekranie"""
		pygame.draw.rect(self.screen, self.color, self.rect)
