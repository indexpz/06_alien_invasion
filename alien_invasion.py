import sys
import pygame  # NOQA
print(pygame.__version__)
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
	"""Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry"""

	def __init__(self):
		"""Inicjalizacja gry i utworzenie jej zasobów"""
		pygame.init()
		self.settings = Settings()
		# Okno gry T1200 × 800.
		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		# Full screen
		# self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		# self.settings.screen_width = self.screen.get_rect().width
		# self.settings.screen_height = self.screen.get_rect().height

		"""Zdefiniowanie koloru tła"""
		self.bg_color = self.settings.bg_color
		pygame.display.set_caption("Inwazja obcych")
		# Utworzenie egzemplarza przechowującego dane statystyczne dotyczące gry.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		# ship
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()
		# 	Utworzenie przycisku gra
		self.play_button = Button(self, "Gra")

	def run_game(self):
		"""Rozpoczęcie pętli głównej gry."""
		while True:
			# Waiting for user reaction click or press button.
			self._check_events()
			# Refreshing screen in every loop
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
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
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_key_down_events(self, event):
		"""Reakcja na naciśnięcie klawisza"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_g:
			self._start_game()

	# elif event.key == pygame.K_f:
	# 	self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	# 	self.settings.screen_width = self.screen.get_rect().width
	# 	self.settings.screen_height = self.screen.get_rect().height

	def _check_key_up_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _check_play_button(self, mouse_pos):
		"""Rozpoczęcie nowej gry po kliknięciu przycisku Gra przez użytkownika."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			# Wyzerowanie danych statystycznych
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self._start_game()
			self.settings.initialize_dynamic_settings()
			# 		Usunięcie list aliens i bullets
			self.aliens.empty()
			self.bullets.empty()
			# 		Utworzenie nowej floty i wyśrodkowanie statku
			self._create_fleet()
			self.ship.center_ship()
			# 		Ukrycie kursora myszy
			# pygame.mouse.set_visable(False)

	def _start_game(self):
		self.stats.game_active = True

	def _fire_bullet(self):
		"""Utworzenie pocisku i dodanie go do grupy pocisków"""
		if len(self.bullets) < self.settings.bullet_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Uaktualnienie położenia pocisków i usunięcie tych niewidocznych na ekranie"""
		# Uaktualnienie położenia pocisków
		self.bullets.update()
		# Usunięcie pocisków, które znajdują się poza ekranem
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		# 	Sprawdzenie, czy którykolwiek pocisk trafił obcego.
		# 	Jeżeli tak, usuwamy zarówno pocisk, jak i obcego.
		self._check_bullet_alien_collision()

	def _check_bullet_alien_collision(self):
		"""Reakcja na kolizję pomiędzy pociskiem a obcym"""
		# 	Usunięcie wszystkich pocisków i obcych, między którymi doszło do kolizji.
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()
		if not self.aliens:
			# Pozbycie się istniejących pocisków i utworzenie nowej floty
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

	def _update_aliens(self):
		"""Sprawdzenie, czy flota znajduje się przy krawędzi, a następnie uaktualnienie położenia wszystkich obcych we flocie"""
		self._check_fleet_edges()
		self.aliens.update()
		# 	Wykrywanie kolizji między obcym a statkiem
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		# 	Wyszukiwanie obcych docierających do dolnej krawędzi ekranu.
		self._check_aliens_bottom()

	def _create_fleet(self):
		"""Tworzy flotę obcych"""
		# 	Utworzenie obcego i ustalenie liczby obcych, którzy zmieszczą się w rzędzie
		# Odległość pomiędzy poszczególnymi obcymi jest równa szerokości obcego
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_of_aliens_x = available_space_x // (2 * alien_width)

		# Ustalenie ile rzędów zmieści się na ekranie
		ship_height = self.ship.rect.height
		available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
		number_rows = available_space_y // (2 * alien_height)

		# Utworzenie pełnej floty
		for row_number in range(number_rows):
			for alien_number in range(number_of_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Utworzenie obcego i umieszczenie go w rzędzie"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Przesunięcie całej floty w dół i zmiana kierunku, w którym się ona porusza"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""Reakcja na uderzenie obcego w statek"""
		if self.stats.ships_left > 0:
			# Zmniejszenie wartości przechowywanej w ships_left
			self.stats.ships_left -= 1

			# 	Usunięcie zawartości list aliens i bullets.
			self.aliens.empty()
			self.bullets.empty()

			# 	Utworzenie nowej floty i wyśrodkowanie statku
			self._create_fleet()
			self.ship.center_ship()
			# 	Pauza
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visable(True)

	def _check_aliens_bottom(self):
		"""Sprawdzanie, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break

	def _update_screen(self):
		# Uaktualnienie obrazów na ekranie i przejście do nowego ekranu.
		self.screen.fill(self.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()  # NOQA
		self.aliens.draw(self.screen)
		# Wyświetlanie informacji o punktacji
		self.sb.show_score()
		# Wyświetlanie przycisku tylko wtedy gdy gra jest nie aktywna
		if not self.stats.game_active:
			self.play_button.draw_button()
		# Display last modifying screen
		pygame.display.flip()
