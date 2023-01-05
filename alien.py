import pygame	# NOQA
from pygame.sprite import Sprite	# NOQA
from settings import Settings


class Alien(Sprite):
	"""Klasa przeznaczona do zarządzania obcym"""

	def __init__(self, ai_game):
		"""Inicjalizacja obcego i jego położenie początkowe"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		# Odczyt obrazu obcego oraz jego pobranie do prostokąta
		self.image = pygame.image.load("images/alien.png")
		self.rect = self.image.get_rect()

		# Każdy nowy obcy pojawia się na górze ekranu
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Położenie obcego jest przechowywane w postaci liczby zmiennoprzecinkowej
		self.x = float(self.rect.x)
		# self.y = float(self.rect.y)

		# Opcje wskazujące na poruszanie się obcego
		# self.moving_right = False
		# self.moving_left = False
		# self.moving_bottom = False

	def update(self):
		"""Uaktualnienie położenia obcego na podstawie opcji wskazującej na jego ruch"""
		# Uaktualnienie wartości współrzędniej X i Y statku, a nie jego prostokąta
		# if self.moving_right and self.rect.right < self.screen_rect.right:
		"""Przesunięcie obcego w prawo lub w lewo"""
		self.x += self.settings.alien_speed * self.settings.fleet_direction
		self.rect.x = self.x
		# if self.moving_left and self.rect.left > 0:
		# 	self.x -= self.settings.alien_speed_x
		# if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
		# 	self.y += self.settings.alien_speed_y

	def check_edges(self):
		"""Zwraca wartość True jeżeli obcy znajduje się przy krawędzi ekranu"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True

# 		Uaktualnienie obiektu rect na podstawie wartości self x i self y
# 		self.rect.x = self.x
# 		self.rect.y = self.y

	# def blitme(self): # NOQA
	# 	"""Wyświetlanie obcego w aktualniej pozycji"""
		# self.screen.blit(self.image, self.rect)
