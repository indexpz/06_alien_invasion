import pygame 	# NOQA
from pygame.sprite import Sprite


class Ship(Sprite):
	"""Klasa przeznaczona do zarządzania statkiem kosmicznym."""

	def __init__(self, ai_game):
		super().__init__()
		# Inicjalizacja statku kosmicznego i jego położenie początkowe.
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()
		# self.settings = Settings()
		self.settings = ai_game.settings

		# Reading ship image and download a rectangle.
		self.image = pygame.image.load("images/ship.png")
		self.rect = self.image.get_rect()

		# Każdy nowy statek kosmiczny pojawia się na dole ekranu.
		self.rect.midbottom = self.screen_rect.midbottom # NOQA

		# Położenie statku jest przechowywane w postaci liczby zmiennoprzecinkowej
		self.x = float(self.rect.x)

		# 	 Opcje wskazujące na poruszanie się statku
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Uaktualnienie położenia statku na podstawie opcji wskazującej na jego ruch"""
		# Uaktualnienie wartości współrzędnej X statku, a nie jego prostokąta.
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		# Uaktualnienie obiektu rect na podstawie wartości self.x.
		self.rect.x = self.x


	def blitme(self): # NOQA
		"""Displaying ship in him actual position"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Umieszczenie statku na środku przy dolnej krawędzi ekranu."""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)