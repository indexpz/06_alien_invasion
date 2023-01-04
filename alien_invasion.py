import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from pilot import Pilot


class AlienInvasion:
	"""Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry"""

	def __init__(self):
		"""Inicjalizacja gry i utworzenie jej zasobów"""
		pygame.init()
		self.settings = Settings()
		# Okno gry 1200x800
		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		# Full screen
		# self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		# self.settings.screen_width = self.screen.get_rect().width
		# self.settings.screen_height = self.screen.get_rect().height

		"""Zdefiniowanie koloru tła"""
		self.bg_color = self.settings.bg_color
		pygame.display.set_caption("Inwazja obcych")
		# ship
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()

	# self.pilot = Pilot(self)

	def run_game(self):
		"""Rozpoczęcie pętli głównej gry."""
		while True:
			# Waiting for user reaction click or press button.
			self._check_events()
			# Refreshing screen in every loop
			self.ship.update()
			self._update_bullets()
			# print(len(self.bullets))
			self._update_screen()

	def _check_events(self):
		# Reakcja na zdarzenia generowane przez klawiaturę i mysz.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_key_down_events(event)
			elif event.type == pygame.KEYUP:
				self._check_key_up_events(event)

	def _check_key_down_events(self, event):
		"""Reakcja na naciśnięcie klawisza"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = Truegit
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		# elif event.key == pygame.K_f:
		# 	self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		# 	self.settings.screen_width = self.screen.get_rect().width
		# 	self.settings.screen_height = self.screen.get_rect().height

	def _check_key_up_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""Utworzenie pocisku i dodanie go do grupy pocisków"""
		if len(self.bullets) < self.settings.bullet_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Uaktualnienie położenia pocisków i usunięcie tych niewidocznych na ekranie"""
	# 	Uaktualnienie położenia pocisków
		self.bullets.update()
		# Usunięcie pocików, które znajdują się poza ekranem
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

	def _update_screen(self):
		# Uaktualnienie obrazów na ekranie i przejście do nowego ekranu.
		self.screen.fill(self.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()  	# NOQA
		# self.pilot.blitme()
		# Display last modifying screen
		pygame.display.flip()
