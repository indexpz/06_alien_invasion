import sys
import pygame

from settings import Settings
from ship import Ship
from pilot import Pilot


class AlienInvasion:
	def __init__(self):
		"""Init game and resources"""
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		self.bg_color = self.settings.bg_color
		pygame.display.set_caption("Inwazja obcych")
		# ship
		self.ship = Ship(self)

	# self.pilot = Pilot(self)

	def run_game(self):
		"""„Rozpoczęcie pętli głównej gry."""
		while True:
			# Waiting for user reaction click or press button.
			self._check_events()
			# Refreshing screen in every loop
			self.ship.update()
			self._update_screen()

	def _check_events(self):
		# Reakcja na zdarzenia generowane przez klawiaturę i mysz.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					self.ship.moving_right = True
				elif event.key == pygame.K_LEFT:
					self.ship.moving_left = True
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					self.ship.moving_right = False
				elif event.key == pygame.K_LEFT:
					self.ship.moving_left = False

	def _update_screen(self):
		# Uaktualnienie obrazów na ekranie i przejście do nowego ekranu.
		self.screen.fill(self.bg_color)
		self.ship.blitme()
		# self.pilot.blitme()
		# Display last modifying screen
		pygame.display.flip()
