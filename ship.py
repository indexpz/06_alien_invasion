import pygame


class Ship:
	"""„Klasa przeznaczona do zarządzania statkiem kosmicznym."""

	def __init__(self, ai_game):
		# „Każdy nowy statek kosmiczny pojawia się na dole ekranu.
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()

		# Reading ship image and download a ractangle.
		self.image = pygame.image.load("images/Ship3.png")
		self.rect = self.image.get_rect()

		# „Każdy nowy statek kosmiczny pojawia się na dole ekranu.
		self.rect.midbottom = self.screen_rect.midbottom

		# 	 Opcje wskazujące na poruszanie się statku
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Uaktualnienie położenia statku na podstawie opcji wskazującej na jego ruch"""
		if self.moving_right:
			self.rect.x += 1
		if self.moving_left:
			self.rect.x -= 1

	def blitme(self):
		"""Displaying ship in him actual position"""
		self.screen.blit(self.image, self.rect)
