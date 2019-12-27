from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Castle(QDialog):

	def __init__(self, parent):
		super(Castle, self).__init__(parent)
		self._dialog = QDialog(self)
		self.setWindowTitle("Zamek")

		self.setStyleSheet("""
				background-image: url(UI/brown_background.jpg);
				background-attachment: scroll;
				border: 2px outset gray;
				border-radius: 10px;
				color: white;
				font-size: 14pt;
				font: Arial;
				min-height: 20px;
			""")

		self.grid = QGridLayout(self)

		self.level1 = self.parent().in_castle_units['level_1']
		self.level2 = self.parent().in_castle_units['level_2']
		self.level3 = self.parent().in_castle_units['level_3']
		self.level4 = self.parent().in_castle_units['level_4']
		self.level5 = self.parent().in_castle_units['level_5']

		self.avaliable1 = self.parent().available_units['level_1']
		self.avaliable2 = self.parent().available_units['level_2']
		self.avaliable3 = self.parent().available_units['level_3']
		self.avaliable4 = self.parent().available_units['level_4']
		self.avaliable5 = self.parent().available_units['level_5']

		self.units = [QLabel('Dostępne:'),
					  QLabel('Jednostki poziomu 1: %d (%d)' % (self.level1, self.avaliable1)),
					  QLabel('Jednostki poziomu 2: %d (%d)' % (self.level2, self.avaliable2)),
					  QLabel('Jednostki poziomu 3: %d (%d)' % (self.level3, self.avaliable3)),
					  QLabel('Jednostki poziomu 4: %d (%d)' % (self.level4, self.avaliable4)),
					  QLabel('Jednostki poziomu 5: %d (%d)' % (self.level5, self.avaliable5))]

		self.upgrade = QPushButton()
		self.upgrade.setText('Ulepsz zamek za 3000 złota')
		self.upgrade.clicked.connect(self.upgrade_castle)
		self.prices = ['60', '100', '400', '1000', '3000']
		self.available = [True, True, False, False, False]
		self.button = []
		self.button_add = []
		for i in range(len(self.prices)):
			self.button.append(QPushButton('Kup jednostkę poziomu %s za %s złota' % (str(i + 1), str(self.prices[i]))))
			self.button_add.append(QPushButton('Dodaj do drużyny'))
		self.button[0].clicked.connect(lambda: self.buy_unit(1))
		self.button[1].clicked.connect(lambda: self.buy_unit(2))
		self.button[2].clicked.connect(lambda: self.buy_unit(3))
		self.button[3].clicked.connect(lambda: self.buy_unit(4))
		self.button[4].clicked.connect(lambda: self.buy_unit(5))

		self.button_add[0].clicked.connect(lambda: self.add_to_team(1))
		self.button_add[1].clicked.connect(lambda: self.add_to_team(2))
		self.button_add[2].clicked.connect(lambda: self.add_to_team(3))
		self.button_add[3].clicked.connect(lambda: self.add_to_team(4))
		self.button_add[4].clicked.connect(lambda: self.add_to_team(5))

	def show_castle(self):
		i = 0
		for label in self.units:
			self.grid.addWidget(label, i, 0)
			i += 1
		if self.parent().castle_level <= 4:# nie wiem czy poziom zamku ma ograniczenie, ale dodaję dla pewności
			self.grid.addWidget(self.upgrade, i, 0, 1, 3)
		close = QPushButton()
		close.setText('Zamknij')
		close.clicked.connect(self._dialog.close)
		self.grid.addWidget(close, i + 1, 0, 1, 3)# Losowo się minimalizuje, nie wiem czemu xD
		for i in range(len(self.prices)):
			if self.available[i]:
				self.grid.addWidget(self.button[i], i + 1, 1)
				self.grid.addWidget(self.button_add[i], i + 1, 2)
			else:
				self.grid.addWidget(QPushButton('Aby odblokować te jednostki musisz ulepszyć zamek'), i + 1, 1, 1, 2)
		self._dialog.setLayout(self.grid)
		self._dialog.exec_()

	def upgrade_castle(self):
		mainWindow = self.parent().parent().parent()
		if self.parent().gold >= 3000:
			self.parent().update_castle_level(self.parent().castle_level+1)
			self.parent().update_gold_amount(self.parent().gold-3000)
			count = self.available.count(True)
			self.available[count] = True
			curr_level = 'level_' + str(count+1)
			self.parent().available_units[curr_level] = 5
			self.update_unit_labels()
			self._dialog.close()
			mainWindow.show_info()
		else:
			print("Masz za mało złota")

	def buy_unit(self, level):
		self.curr_level = 'level_' + str(level)  # potrzebuję ziennej level osobno
		self.max_units = self.parent().available_units[self.curr_level]
		if self.max_units is not 0:
			self._dialog_buy = QDialog()
			self._dialog_buy.setStyleSheet("""
										background-image: url(UI/brown_background.jpg);
										background-attachment: scroll;
										border: 2px outset gray;
										border-radius: 10px;
										color: white;
										font-size: 14pt;
										font: Arial;
										min-height: 20px; """)
			self._dialog_buy.setWindowTitle("Kup jednostki")
			layout = QVBoxLayout(self._dialog_buy)
			text = QLabel("Ile jednostek chcesz kupić?")

			hlay = QHBoxLayout()
			minus = QPushButton('-')
			minus.setStyleSheet("min-width: 20px; max-width: 20px;")
			minus.clicked.connect(self.substract)
			self.slider_buy = QSlider(Qt.Horizontal)
			self.slider_buy.setValue(1)
			self.slider_buy.setMaximum(self.max_units)
			self.slider_buy.valueChanged[int].connect(self.changeValue)
			plus = QPushButton('+')
			plus.setStyleSheet("min-width: 20px; max-width: 20px;")
			plus.clicked.connect(self.add)
			self.value = QLabel()
			self.value.setAlignment(Qt.AlignCenter)
			self.value.setText(str(1))
			self.price = int(self.prices[level-1])
			self.to_pay = self.price

			self.full_price = QLabel("Suma do zapłaty: %d" % self.price)# taki napis?

			hlay.addWidget(minus)
			hlay.addWidget(self.slider_buy)
			hlay.addWidget(plus)

			buy = QPushButton()
			buy.setText("Kup")
			buy.clicked.connect(self.buy)
			cancel = QPushButton()
			cancel.setText("Anuluj")
			cancel.clicked.connect(self._dialog_buy.close)

			layout.addWidget(text)
			layout.addLayout(hlay)
			layout.addWidget(self.value)
			layout.addWidget(self.full_price)

			layout.addWidget(buy)
			layout.addWidget(cancel)
			self._dialog_buy.setLayout(layout)
			self._dialog_buy.exec_()
		else:
			print("Brak dostępnych jednostek do kupienia")

	def buy(self):
		mainWindow = self.parent().parent().parent()
		if self.parent().gold >= self.to_pay: #pozwala ci kupić tylko jak cię stać, jak nie to nic nie robi/ wypisuje, że cię nie stać
			self.parent().update_gold_amount(self.parent().gold - self.to_pay)
			self.parent().available_units[self.curr_level] -= self.slider_buy.value()
			self.parent().in_castle_units[self.curr_level] += self.slider_buy.value()
			self._dialog_buy.close()
			self.update_unit_labels()
			mainWindow.show_info()
		else:
			print("Za mało złota")

	def substract(self):
		value = self.slider_buy.value()
		if value is not 0:
			self.slider_buy.setValue(value-1)

	def changeValue(self, value):
		self.value.setText(str(value))
		self.to_pay = self.price * value
		self.full_price.setText("Suma do zapłaty: %d" % self.to_pay)

	def add(self):
		value = self.slider_buy.value()
		if value is not self.max_units:
			self.slider_buy.setValue(value+1)

	def add_to_team(self, level):
		self.curr_level = 'level_' + str(level)
		self.max_units = self.parent().in_castle_units[self.curr_level]
		if self.max_units is not 0:
			self._dialog_team = QDialog()
			self._dialog_team.setStyleSheet("""
										background-image: url(UI/brown_background.jpg);
										background-attachment: scroll;
										border: 2px outset gray;
										border-radius: 10px;
										color: white;
										font-size: 14pt;
										font: Arial;
										min-height: 20px; """)
			self._dialog_team.setWindowTitle("Dodaj jednostki do drużyny")
			layout = QVBoxLayout(self._dialog_team)
			text = QLabel("Ile jednostek chcesz dodać?")

			hlay = QHBoxLayout()
			minus = QPushButton('-')
			minus.setStyleSheet("min-width: 20px; max-width: 20px;")
			minus.clicked.connect(self.substract_team)
			self.slider_team = QSlider(Qt.Horizontal)
			self.slider_team.setValue(1)
			self.slider_team.setMaximum(self.max_units)
			self.slider_team.valueChanged[int].connect(self.changeValue_team)
			plus = QPushButton('+')
			plus.setStyleSheet("min-width: 20px; max-width: 20px;")
			plus.clicked.connect(self.add_team)
			self.value = QLabel()
			self.value.setAlignment(Qt.AlignCenter)
			self.value.setText(str(1))

			hlay.addWidget(minus)
			hlay.addWidget(self.slider_team)
			hlay.addWidget(plus)

			team = QPushButton()
			team.setText("Dodaj")
			team.clicked.connect(self.team)
			cancel = QPushButton()
			cancel.setText("Anuluj")
			cancel.clicked.connect(self._dialog_team.close)

			layout.addWidget(text)
			layout.addLayout(hlay)
			layout.addWidget(self.value)

			layout.addWidget(team)
			layout.addWidget(cancel)
			self._dialog_team.setLayout(layout)
			self._dialog_team.exec_()
		else:
			print("Brak dostępnych jednostek do dodania")

	def team(self):
		mainWindow = self.parent().parent().parent()
		hero = self.parent().hero
		if hero is 1:
			self.parent().h1units[self.curr_level] += self.slider_team.value()
			#print("h1 %s" % self.parent().h1units)
		elif hero is 2:
			self.parent().h2units[self.curr_level] += self.slider_team.value()
			#print("h2 %s" % self.parent().h2units)
		else:
			self.parent().h3units[self.curr_level] += self.slider_team.value()
			#print("h3 %s" % self.parent().h3units)
		self.parent().in_castle_units[self.curr_level] -= self.slider_team.value()
		self.update_unit_labels()
		self._dialog_team.close()
		self.show_castle()
		mainWindow.show_info()# chyba nie terzeba odświeżać

	def substract_team(self):
		value = self.slider_team.value()
		if value is not 0:
			self.slider_team.setValue(value-1)

	def changeValue_team(self, value):
		self.value.setText(str(value))

	def add_team(self):
		value = self.slider_team.value()
		if value is not self.max_units:
			self.slider_team.setValue(value+1)

	def update_unit_labels(self):
		for level in range(len(self.available)):
			curr_level = 'level_' + str(level+1)
			self.units[level+1].setText("Jednostki poziomu %d: %d (%d)" % (level+1, self.parent().in_castle_units[curr_level], self.parent().available_units[curr_level]))

