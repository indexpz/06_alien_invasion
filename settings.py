class Settings:
	def __init__(self):
		"""Inicjalizacja danych statycznych gry"""
		# Ustawienia dotyczące ekranu
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (60, 0, 60)
		# Ustawienia dotyczące statku
		self.ship_limit = 3
		# Ustawienia dotyczące pocisku
		self.bullet_width = 300
		self.bullet_height = 15
		self.bullet_color = (255, 255, 255)
		self.bullet_allowed = 5
		# Ustawienia dotyczące obcego
		self.fleet_drop_speed = 10
		# 		Łatwa zmiana szybkości gry
		self.speedup_scale = 1.1
		# Łatwa zmiana liczby punktów przyznawanych za zestrzelenie obcego
		self.score_scale = 1.5
		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Inicjalizacja ustawień, które ulegają zmianie w trakcie gry."""
		self.ship_speed = 3.5
		self.bullet_speed = 1.5
		self.alien_speed = 1.0
		# Wartość fleet_direction wynosząca 1 oznacza prawo, natomiast -1 oznacza lewo
		self.fleet_direction = 1
		self.alien_points = 50

	def increase_speed(self):
		"""Zmiana ustawień dotyczących szybkości"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
		# print(self.alien_points)
