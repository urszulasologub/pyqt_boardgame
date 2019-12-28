import os, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from dice import DiceRoll
from castle import Castle
import math
from battle import *
from random import randrange


class PlayerInfo(QWidget):
	def __init__(self, parent, player, castle_x, castle_y):
		self.castle_x = castle_x
		self.castle_y = castle_y
		self.castle_level = 1
		self.gold = 0
		self.dice = 0
		self.h1pos_x = 0
		self.h1pos_y = 0
		self.h2pos_x = 0
		self.h2pos_y = 0
		self.h3pos_x = 0
		self.h3pos_y = 0
		self.available_heroes = [1]
		self.hero = 1
		self.can_move = False

		self.h1units = {
			"level_1": 15,
			"level_2": 10,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0,
		}

		self.h2units = {
			"level_1": 15,
			"level_2": 10,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}

		self.h3units = {
			"level_1": 15,
			"level_2": 10,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}

		self.in_castle_units = {
			"level_1": 10,
			"level_2": 5,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}

		self.available_units = {
			"level_1": 10,
			"level_2": 5,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}# powiedzmy, że od razu może kupić 5, poza poziomem 1

		super(PlayerInfo, self).__init__(parent)
		color = 'darkblue'
		if player == 'Gracz 1':
			color = 'darkred'
		self.setStyleSheet("""
			QDialog, QLabel, QPushButton {
			background-image: url(UI/brown_background.jpg);
			background-attachment: scroll;
			border: 2px outset %s;
			border-radius: 10px;
			color: white;
			font-size: 18pt;
			font: Arial;
			min-height: 15px;}
			
			QPushButton:pressed {
			background-image: url(UI/darker_brown_background.jpg);}
			""" % color)
		self.grid = QGridLayout(self)
		self.castle = Castle(self)
		castle_image = QPushButton()
		castle_image.setStyleSheet('border-image: url(UI/castle_inside); min-height: 200px; ')
		castle_image.clicked.connect(self.show_castle)

		self.grid.addWidget(castle_image, 0, 0)

		self.labels = [QLabel(player), QLabel('Poziom zamku: %d' % self.castle_level), QLabel('Złoto: 0'), QLabel('Wyrzucono oczek: %d' % self.dice), QLabel('Tydzień: %d, Dzień: %d' % (self.parent().week, self.parent().day))]

		i = 1
		for label in self.labels:
			self.grid.addWidget(label, i, 0)
			i += 1

		self.setLayout(self.grid)
		self.update_gold_amount(5000)
		#self.update_week_day()

	def show_castle(self):
		self.castle.show_castle()

	def update_castle_level(self, level):
		self.castle_level = level
		text = 'Poziom zamku: ' + str(level)
		self.labels[1] = QLabel(text)
		self.grid.addWidget(self.labels[1], 2, 0)

	def update_gold_amount(self, amount):
		self.gold = amount
		text = 'Złoto: ' + str(amount)
		self.labels[2] = QLabel(text)
		self.grid.addWidget(self.labels[2], 3, 0)

	def update_dice_amount(self, amount):
		self.dice = amount
		text = 'Wyrzucono oczek: ' + str(amount)
		self.labels[3] = QLabel(text)
		self.grid.addWidget(self.labels[3], 4, 0)

	def update_week_day(self, week, day): # z jakiegoś powodu, jak się używa parent() to wywala cały program
		text = 'Tydzień: ' + str(week) + ', Dzień: ' + str(day)
		self.labels[4] = QLabel(text)
		self.grid.addWidget(self.labels[4], 5, 0)

	def clear_hero_pos(self, hero_num):
		if hero_num == 1:
			self.h1pos_x = self.castle_x
			self.h1pos_y = self.castle_y
		elif hero_num == 2:
			self.h2pos_x = self.castle_x
			self.h2pos_y = self.castle_y
		else:
			self.h3pos_x = self.castle_x
			self.h3pos_y = self.castle_y

#akcje zawsze są te same, więc nie potrzeba podawać gracza
class PlayerActions(QWidget):
	def __init__(self, parent):
		super(PlayerActions, self).__init__(parent)
		self.main_window = self.parent().parent()
		self.board = self.parent()
		self.setStyleSheet("""
			QDialog, QLabel, QPushButton {
			background-image: url(UI/brown_background.jpg);
			background-attachment: scroll;
			border: 2px outset gray;
			border-radius: 10px;
			color: white;
			font-size: 18pt;
			font: Arial;
			min-height: 50px;}
			
			QPushButton:pressed {
			background-image: url(UI/darker_brown_background.jpg);}
			""")

		self.grid = QGridLayout(self)
		self.labels = ['Zobacz druzynę', 'Zakończ kolejkę', 'Atakuj', 'Bohater1', 'Bohater2', 'Bohater3', 'Wykonaj ruch']
		self.buttons = []

		for i in range(len(self.labels)):
			self.buttons.append(QPushButton(self.labels[i]))
			self.grid.addWidget(self.buttons[i], i, 0)

		self.buttons[0].clicked.connect(self.show_team)
		self.buttons[1].clicked.connect(self.change_turn)
		self.buttons[2].clicked.connect(self.start_combat)
		self.buttons[3].clicked.connect(self.set_hero_one)
		self.buttons[4].clicked.connect(self.set_hero_two)
		self.buttons[5].clicked.connect(self.set_hero_three)
		self.buttons[6].clicked.connect(self.move)
		self.setLayout(self.grid)

	def start_combat(self):
		if self.main_window.turn % 2 is 1:
			whose_turn = self.main_window.player1
			attacked = self.main_window.player2
		else:
			whose_turn = self.main_window.player2
			attacked = self.main_window.player1
		if whose_turn.hero is not None:
			if whose_turn.hero == 1:
				x = whose_turn.h1pos_x
				y = whose_turn.h1pos_y
			elif whose_turn.hero == 2:
				x = whose_turn.h2pos_x
				y = whose_turn.h2pos_y	
			elif whose_turn.hero == 3:	
				x = whose_turn.h3pos_x
				y = whose_turn.h3pos_y
			opponent = self.board.get_opponent_on_tile(x, y)	
			if opponent:	
				battle = Battle(whose_turn, attacked, str(whose_turn.hero), opponent[0])
				raport = battle.generate_battle_raport()
				battle.update_loser(battle.loser, battle.lost_hero)
				battle_dialog = BattleDialog(self, battle, whose_turn)
			else:
				self._dialog = QDialog(self)
				self._dialog.setWindowTitle('!')
				self._dialog.setStyleSheet("""
					background-image: url(UI/brown_background.jpg);
					background-attachment: scroll;
					border: 2px outset gray;
					border-radius: 10px;
					color: white;
					font-size: 18pt;
					font: Arial;
					min-height: 15px;
					""")
				layout = QVBoxLayout()  # Pierwszy lepszy layout
				text = QLabel('Nie ma zadnego przeciwnika')
				layout.addWidget(text)
				self._dialog.setLayout(layout)
				self._dialog.exec_()

	def move(self):
		if self.main_window.turn % 2 is 0:
			hero = self.main_window.player2.hero
			player = self.main_window.player2
		else:
			hero = self.main_window.player1.hero
			player = self.main_window.player1

		if player.can_move and hero is not None:
			tile = self.move_hero(player, hero, self.main_window.height, self.main_window.width)
			player.can_move = False
			#Zmienić wartoś nowej zmiennej, że już się ruszył
			self.main_window.show_info()
			for special_location in self.main_window.special_locations:
				print(tile, special_location)
				if tile == special_location:
					print('\nPole specjalne!\n')
					self.handle_special_tile(player, hero, tile)
					break
		else:
			self._dialog = QDialog(self)
			self._dialog.setWindowTitle('!')
			self._dialog.setStyleSheet("""
				background-image: url(UI/brown_background.jpg);
				background-attachment: scroll;
				border: 2px outset gray;
				border-radius: 10px;
				color: white;
				font-size: 18pt;
				font: Arial;
				min-height: 15px;
				""")
			layout = QVBoxLayout() #Pierwszy lepszy layout
			text = QLabel('Już się ruszyłeś w tej turze')
			layout.addWidget(text)
			self._dialog.setLayout(layout)
			self._dialog.exec_()


	def handle_special_tile(self, player, hero, location):
		situations = { 'easy_fight': self.random_fight(player, hero, 'easy', location),
					'medium_fight': 'medium_fight',
					'hard_fight': 'hard_fight',
					'small_prize': 'small_prize',
					'medium_prize': 'medium_prize',
					'big_prize': 'big_prize' }		
		rand = randrange(1, 101)
		if rand < 28:
			situation = situations['easy_fight']
		elif rand < 65:
			situation = situations['small_prize']
		elif rand < 80:
			situation = situations['medium_fight']
		elif rand < 95:
			situation = situations['medium_prize']
		elif rand < 98:
			situation = situations['big_prize']
		else:
			situation = situations['hard_fight']

		print(situation)
		

	def random_fight(self, player, hero, level, location):
		bot = PlayerInfo(self.main_window, 'bot', None, None)
		bot.h1pos_x = location[0]
		bot.h2pos_x = location[1]
		multiplier = self.main_window.week
		if level == 'easy':
			bot.h1units = {
				'level_1': int(randrange(10) * multiplier),
				'level_2': int(randrange(2) * multiplier),
				'level_3': 0,
				'level_4': 0,
				'level_5': 0
			}
		battle = Battle(bot, player, '1', str(hero))
		raport = battle.generate_battle_raport()
		battle_dialog = BattleDialog(self, battle, player)
		del bot

		

	def move_hero(self, player, hero, height, width):
		x = None
		y = None
		if hero is 1:# muszę w ten sposób, z dodatkowa zmienna na player.h1pos_x itd, nie działa
			#print("=====")
			for i in range(player.dice):  # pętli, żeby nie wyszło za przedział
				if player.h1pos_x in range(width - 1) and player.h1pos_y is 0:
					#print("lewo")
					player.h1pos_x += 1
				elif player.h1pos_x is 0 and player.h1pos_y in range(width - 1):
					#print("gora")
					player.h1pos_y -= 1
				elif player.h1pos_x in range(width) and player.h1pos_y is height - 1:
					#print("prawo")
					player.h1pos_x -= 1
				elif player.h1pos_x is width - 1 and player.h1pos_y in range(height):
					#print("dol")
					player.h1pos_y += 1
			x = player.h1pos_x
			y = player.h1pos_y
		elif hero is 2:
			for i in range(player.dice):
				if player.h2pos_x in range(width - 1) and player.h2pos_y is 0:
					player.h2pos_x += 1
				elif player.h2pos_x is 0 and player.h2pos_y in range(width - 1):
					player.h2pos_y -= 1
				elif player.h2pos_x in range(width) and player.h2pos_y is height - 1:
					player.h2pos_x -= 1
				elif player.h2pos_x is width - 1 and player.h2pos_y in range(height):
					player.h2pos_y += 1
			x = player.h2pos_x
			y = player.h2pos_y
		else:
			for i in range(player.dice):
				if player.h3pos_x in range(width - 1) and player.h3pos_y is 0:
					player.h3pos_x += 1
					x = player.h3pos_x
				elif player.h3pos_x is 0 and player.h3pos_y in range(width - 1):
					player.h3pos_y -= 1
					y = player.h3pos_y
				elif player.h3pos_x in range(width) and player.h3pos_y is height - 1:
					player.h3pos_x -= 1
					x = player.h3pos_x 
				elif player.h3pos_x is width - 1 and player.h3pos_y in range(height):
					player.h3pos_y += 1
					y = player.h3pos_y
			x = player.h3pos_x
			y = player.h3pos_y
		return (x, y)

	def change_turn(self):
		self.main_window.turn += 1
		#print(self.main_window.turn)
		self.main_window.roll_dice()
		self.main_window.show_info()

	def buy_new_hero(self, player, hero):
		self._dialog = QDialog()
		self._dialog.setStyleSheet("""
			QDialog, QLabel, QPushButton {
			background-image: url(UI/brown_background.jpg);
			background-attachment: scroll;
			border: 2px outset gray;
			border-radius: 10px;
			color: white;
			font-size: 18pt;
			font: Arial;
			min-height: 20px;}
			
			QPushButton:pressed {
			background-image: url(UI/darker_brown_background.jpg);}
			""")
		self._dialog.setWindowTitle("Kup bohatera")
		layout = QVBoxLayout(self._dialog)#tymczasowo
		text = QLabel()
		text.setText("Kupić bohatera za 1500 sztuk złota?")
		buy = QPushButton()
		buy.setText("Kup")
		buy.clicked.connect(lambda: self.buy(player, hero))
		cancel = QPushButton()
		cancel.setText("Anuluj")
		cancel.clicked.connect(self._dialog.close)
		layout.addWidget(text)
		layout.addWidget(buy)
		layout.addWidget(cancel)

		self._dialog.setLayout(layout)
		self._dialog.show()


	def buy(self, player, hero):
		if player is 1 and self.main_window.player1.gold >= 1500:
			self.main_window.player1.available_heroes.append(hero)
			self.main_window.player1.hero = hero
			self.main_window.player1.update_gold_amount(self.main_window.player1.gold - 1500)
			if hero is 1:
				self.board.set_hero(0, 0, self.board.player1_button)
			elif hero is 2:
				self.board.set_hero_2(0, 0, self.board.player1_button2)
			else:
				self.board.set_hero_3(0, 0, self.board.player1_button3)
		elif player is 2 and self.main_window.player2.gold >= 1500:
			self.main_window.player2.available_heroes.append(hero)
			self.main_window.player2.hero = hero
			self.main_window.player2.update_gold_amount(self.main_window.player2.gold - 1500)
			pos = [self.board.parent().width - 1, self.board.parent().height - 1]
			if hero is 1:
				self.board.set_hero(pos[0], pos[1], self.board.player2_button)
			elif hero is 2:
				self.board.set_hero_2(pos[0], pos[1], self.board.player2_button2)
			else:
				self.board.set_hero_3(pos[0], pos[1], self.board.player2_button3)
		self._dialog.close()


	def set_hero_one(self):
		if self.main_window.turn % 2 is 0:
			if 1 in self.main_window.player2.available_heroes:
				self.main_window.player2.hero = 1
			else:
				self.buy_new_hero(2, 1)
		else:
			if 1 in self.main_window.player1.available_heroes:
				self.main_window.player1.hero = 1
			else:
				self.buy_new_hero(1, 1)


	def set_hero_two(self):
		if self.main_window.turn % 2 is 0:
			if 2 in self.main_window.player2.available_heroes:
				self.main_window.player2.hero = 2
			else:
				self.buy_new_hero(2, 2)
		else:
			if 2 in self.main_window.player1.available_heroes:
				self.main_window.player1.hero = 2
			else:
				self.buy_new_hero(1, 2)


	def set_hero_three(self):
		if self.main_window.turn % 2 is 0:
			if 3 in self.main_window.player2.available_heroes:
				self.main_window.player2.hero = 3
			else:
				self.buy_new_hero(2, 3)
		else:
			if 3 in self.main_window.player1.available_heroes:
				self.main_window.player1.hero = 3
			else:
				self.buy_new_hero(1, 3)

	def show_team(self):
		self._dialog = QDialog()
		self._dialog.setStyleSheet("""
			QDialog, QLabel, QPushButton {
			background-image: url(UI/brown_background.jpg);
			background-attachment: scroll;
			border: 2px outset gray;
			border-radius: 10px;
			color: white;
			font-size: 18pt;
			font: Arial;
			min-height: 20px;}
			
			QPushButton:pressed {
			background-image: url(UI/darker_brown_background.jpg);}
			""")
		self._dialog.setWindowTitle('Drużyna')
		if self.main_window.turn % 2 is 0:
			player = self.main_window.player2
			hero = self.main_window.player2.hero
		else:
			player = self.main_window.player1
			hero = self.main_window.player1.hero
		if hero is 1:
			units = player.h1units
		elif hero is 2:
			units = player.h2units
		else:
			units = player.h3units
		layout = QVBoxLayout()
		if hero is not None:
			labels = [QLabel('Drużyna bohatera %d' % hero),
					QLabel('Jednostki poziomu 1: %d' % units['level_1']),
					QLabel('Jednostki poziomu 2: %d' % units['level_2']),
					QLabel('Jednostki poziomu 3: %d' % units['level_3']),
					QLabel('Jednostki poziomu 4: %d' % units['level_4']),
					QLabel('Jednostki poziomu 5: %d' % units['level_5'])]
			for label in labels:
				layout.addWidget(label)
		else:
			layout.addWidget(QLabel('Nie wybrano bohatera'))
		self._dialog.setLayout(layout)
		self._dialog.exec_()

