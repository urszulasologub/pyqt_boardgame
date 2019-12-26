import os, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from player import *
from dice import DiceRoll
from random import randrange


class Battle():
	def __init__(self, parent, attacking_player, attacked_player, hero1, hero2):
		self.attacking_player = attacking_player		#type: PlayerInfo
		self.attacked_player = attacked_player
		#attacking player always starts battle
		attacking_dict = {'1': self.attacking_player.h1units,
					'2': self.attacking_player.h2units,
					'3': self.attacking_player.h3units,
					'castle': self.attacking_player.in_castle_units }
		attacked_dict = {'1': self.attacked_player.h1units,
					'2': self.attacked_player.h2units,
					'3': self.attacked_player.h3units,
					'castle': self.attacked_player.in_castle_units }
		self.attacking_hero = attacking_dict(hero1)
		self.attacked_hero = attacked_dict(hero2)

		self.unit_atk = {
			"level_1": 6,
			"level_2": 9,
			"level_3": 12,
			"level_4": 16,
			"level_5": 30
		}

		self.unit_health = {
			"level_1": 10,
			"level_2": 25,
			"level_3": 40,
			"level_4": 100,
			"level_5": 250
		}


	def generate_battle_raport(self):
		self.raport = "Raport z walki\n"

		attacked_health = {
			'level_1': self.unit_health['level_1'] * self.attacked_hero['level_1'],
			'level_2': self.unit_health['level_2'] * self.attacked_hero['level_2'],
			'level_3': self.unit_health['level_3'] * self.attacked_hero['level_3'],
			'level_4': self.unit_health['level_4'] * self.attacked_hero['level_4'],
			'level_5': self.unit_health['level_5'] * self.attacked_hero['level_5']
		}

		attacking_health = {
			'level_1': self.unit_health['level_1'] * self.attacking_hero['level_1'],
			'level_2': self.unit_health['level_2'] * self.attacking_hero['level_2'],
			'level_3': self.unit_health['level_3'] * self.attacking_hero['level_3'],
			'level_4': self.unit_health['level_4'] * self.attacking_hero['level_4'],
			'level_5': self.unit_health['level_5'] * self.attacking_hero['level_5']
		}
		
		while self.health(attacking_health) > 0 and self.health(attacked_health) > 0:
			pass

		if self.health(self.attacking_hero) > 0:
			self.winner = self.attacking_hero
		else:
			self.winner = self.attacked_hero
		return self.winner


	def health(self, health_dict):
		return health_dict['level_1'] + health_dict['level_2'] + health_dict['level_3'] + health_dict['level_4'] + health_dict['level_5']


	def attack(self, player1, player2, level, health):
		if player1[level] > 0:
			dice = randrange(1, 7)
			self.raport += "Wyrzucono %d oczek.\n" % dice
			if dice is 6:
				self.raport += 'Cios krytyczny! '
			multiplier = { 1: 0.2,
						2: 0.7,
						3: 0.85, 
						4: 1, 
						5: 1.2,
						6: 2 }
			damage = int((multiplier[dice] * self.unit_atk[level]) * (1 + (player1[level] * 0.01)))
			self.raport += 'Jednostka poziomu %d zadała %d obrazeń. ' % (level, damage)

			health -= damage
		return health


		

	


