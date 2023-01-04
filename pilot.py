import pygame


class Pilot:
	def __init__(self, ai_game):
		#  inicjalizacja postaci
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()
		# Pobieranie obrazu postaci i prostokąta
		self.image = pygame.image.load("images/person.png")
		# self.image = pygame.Surface(self.image.get_size()).convert_alpha()
		# self.image.fill((255, 0, 0))
		self.rect = self.image.get_rect()

		# Pojawienie się postaci na środku
		self.rect.center = self.screen_rect.center

	def blitme(self):
		# pokazuje pilota w aktualnej pozycji
		self.screen.blit(self.image, self.rect)
