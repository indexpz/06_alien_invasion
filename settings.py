class Settings:
	def __init__(self):
		"""Initialization game settings"""
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (60, 0, 60)

		# 		Ustawienia dotyczące statku
		self.ship_speed = 3.5

		# 		Ustawienia dotyczące pocisku
		self.bullet_speed = 1.0
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullet_allowed = 3
