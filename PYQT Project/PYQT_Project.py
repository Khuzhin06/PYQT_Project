from PIL import Image, ImageDraw
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from random import randint, choice
from finaly_project import Ui_Dialog
from Second_form import Second_form
import sqlite3
import datetime
from PyQt5.QtWidgets import QInputDialog, QColorDialog


class Draw_maker(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.for_forest_field = ['self.checkBox_path.setEnabled(True)',
                                 'self.checkBox_boat.setEnabled(False)', 'self.checkBox_boat.setChecked(False)',
                                 'self.spinBox_boat.setEnabled(False)', 'self.tree.setEnabled(True)',
                                 'self.checkBox_lighthouse.setEnabled(False)',
                                 'self.checkBox_lighthouse.setChecked(False)',
                                 'self.spinBox_lighthouse.setEnabled(False)', 'self.checkBox_fish.setEnabled(False)',
                                 'self.checkBox_fish.setChecked(False)', 'self.spinBox_fish.setEnabled(False)',
                                 ]  # Записываем при изменении как для леса и для поляны
        self.color_down = '#13942b'
        self.down = {self.radioButton_ocean: '#2663de',
                     self.radioButton_field: '#7bd444',
                     self.radioButton_forest: '#06782e'}
        self.sl = {self.tree: 'self.make_tree', self.checkBox_boat: 'self.make_boat',
                   self.checkBox_house: 'self.make_house',
                   self.checkBox_animals: 'self.make_animals',
                   self.checkBox_fish: 'self.make_fish',
                   self.checkBox_fence: 'self.make_fence',
                   self.checkBox_lighthouse: 'self.make_lighthouse'
                   }
        self.spin = {self.tree: [self.spinBox_tree],
                     self.checkBox_boat: [self.spinBox_boat],
                     self.checkBox_house: [self.spinBox_house, self.checkBox],
                     self.checkBox_path: [self.spinBox_path],
                     self.checkBox_cloud: [self.spinBox_cloud],
                     self.mount: [self.spinBox_mount],
                     self.checkBox_fence: [self.spinBox_fence],
                     self.checkBox_lighthouse: [self.spinBox_lighthouse],
                     self.checkBox_fish: [self.spinBox_fish],
                     self.checkBox_animals: [self.spinBox_animals],
                     self.time: [self.radioButton_day, self.radioButton_night, self.radioButton_now,
                                 self.radioButton_morning, self.radioButton_evening],
                     self.season: [self.radioButton_auttom, self.radioButton_summer, self.radioButton_now_season,
                                   self.radioButton_spring, self.radioButton_winter]}  # Словарь кнопок
        self.restart_new = {
            self.radioButton_ocean: ['self.checkBox_boat.setEnabled(True)', 'self.checkBox_path.setChecked(False)',
                                     'self.tree.setEnabled(False)',
                                     'self.tree.setChecked(False)',
                                     'self.checkBox_path.setEnabled(False)',
                                     'self.checkBox_animals.setEnabled(False)',
                                     'self.checkBox_animals.setChecked(False)',
                                     'self.spinBox_animals.setEnabled(False)',
                                     'self.checkBox_fence.setEnabled(False)',
                                     'self.checkBox_fence.setChecked(False)', 'self.spinBox_fence.setEnabled(False)',
                                     'self.checkBox_lighthouse.setEnabled(True)', 'self.checkBox_fish.setEnabled(True)'
                                     ],
            self.radioButton_forest: self.for_forest_field + ['self.spinBox_tree.setMinimum(19)',
                                                              'self.spinBox_tree.setMaximum(34)',
                                                              'self.checkBox_animals.setEnabled(True)',
                                                              'self.checkBox_fence.setEnabled(False)',
                                                              'self.checkBox_fence.setChecked(False)',
                                                              'self.spinBox_fence.setEnabled(False)',
                                                              ],
            self.radioButton_field: self.for_forest_field + ['self.spinBox_tree.setMaximum(8)',
                                                             'self.spinBox_tree.setMinimum(1)',
                                                             'self.checkBox_fence.setEnabled(True)',
                                                             'self.checkBox_animals.setEnabled(False)',
                                                             'self.checkBox_animals.setChecked(False)',
                                                             'self.spinBox_animals.setEnabled(False)'
                                                             ]}  # Для перезапуска при изменение основной части

        self.i = -2  # Колличество  разных предметов что будут на картинке для прогресс бара

        self.day_id = '3'
        self.spin_day = {self.radioButton_day: '3', self.radioButton_night: '5',
                         self.radioButton_morning: '2', self.radioButton_evening: '4'}

        self.season_id = '4'  # записываем ID дня и сезона года где происходит картинка, по умолчанию может в любом
        self.spin_season = {self.radioButton_auttom: '5', self.radioButton_summer: '4',
                            self.radioButton_spring: '3', self.radioButton_winter: '2'}

        self.radioButton_ocean.toggled.connect(self.restart)  # Основы
        self.radioButton_forest.toggled.connect(self.restart)
        self.radioButton_field.toggled.connect(self.restart)

        self.tree.stateChanged.connect(self.spin_check)
        self.checkBox_boat.stateChanged.connect(self.spin_check)  # Подключаем кнопки включения и сколько будет
        self.checkBox_house.stateChanged.connect(self.spin_check)
        self.checkBox_path.stateChanged.connect(self.spin_check)
        self.checkBox_cloud.stateChanged.connect(self.spin_check)
        self.mount.stateChanged.connect(self.spin_check)
        self.time.stateChanged.connect(self.spin_check)
        self.season.stateChanged.connect(self.spin_check)
        self.checkBox_lighthouse.stateChanged.connect(self.spin_check)
        self.checkBox_fence.stateChanged.connect(self.spin_check)
        self.checkBox_fish.stateChanged.connect(self.spin_check)
        self.checkBox_animals.stateChanged.connect(self.spin_check)
        self.checkBox_sun.stateChanged.connect(self.spin_sun)
        self.checkBox.stateChanged.connect(self.color_change)

        self.pushButton.clicked.connect(self.make_draw)

    def make_tree(self, gde_y, color_trunk='#331a00', color_foliage='#3b7d0c'):
        if self.tree.checkState():
            color_trunk = self.db(1)
            color_foliage = self.db(17, season=True)
            gde_x = randint(100, 1000)
            if gde_y >= 500:
                a = 55
            elif gde_y >= 370:
                a = 30
            elif gde_y >= 200:
                a = 15
            self.drawer.rectangle(((gde_x - a, gde_y - a * 4), (gde_x, gde_y)), color_trunk)
            self.drawer.ellipse(((gde_x - a * 1.6, gde_y - a * 6), (gde_x + a * 0.6, gde_y - a * 2)), color_foliage)

    def make_cloud(self, gde_y, color='#d0d7d9'):
        if self.checkBox_cloud.checkState():
            gde_x = randint(250, 1000)
            if self.delenie == 500:
                a = 40
            elif self.delenie == 350:
                a = 30
            elif self.delenie == 200:
                a = 15
            self.drawer.ellipse(((gde_x - a * 1.5, gde_y - a * 2), (gde_x + a * 0.5, gde_y)), color)
            self.drawer.ellipse(((gde_x - a * 3, gde_y - a * 2), (gde_x - a, gde_y)), color)
            self.drawer.ellipse(((gde_x - a * 4.5, gde_y - a * 2), (gde_x - 2 * a, gde_y)), color)
            self.drawer.ellipse(((gde_x - a * 3, gde_y - a * 3), (gde_x - a, gde_y - a)), color)

    def make_house(self, gde_y, color='#855a1d', color_2='#851d22', color_3='#543310', color_4='#24ede6'):
        if self.checkBox_house.checkState():
            color_3 = self.db(1)
            color = self.db(2)
            if self.checkBox.checkState():
                color_2 = self.color_roof.name()
                a = self.cur.execute(
                    "SELECT cod FROM color_main WHERE color = 3 and season = 2").fetchone()
                print(a)
                if a is None:
                    self.cur.execute(
                        f"INSERT INTO color_main(cod,color,day,season) VALUES ('{str(self.color_roof.name())}', 3, 3, 2)")
                    self.con.commit()
                else:
                    self.cur.execute(f"UPDATE color_main SET cod = 'str(self.color_roof.name())' WHERE color = '3' and season = '2'")
                    self.con.commit()
            else:
                color_2 = self.db(3)
            color_4 = self.db(11)
            gde_x = randint(200, 1000)
            if gde_y >= 500:
                a = 40
            elif gde_y >= 370:
                a = 25
            elif gde_y >= 200:
                a = 15

            if self.radioButton_ocean.isChecked():  # Если это океан то мы уменьшаем размер дома
                a = a // 2.5

            self.drawer.rectangle(((gde_x - a * 5, gde_y - a * 3.5), (gde_x, gde_y)), color)
            self.drawer.polygon(((gde_x, gde_y - a * 3.5),
                                 (gde_x - a * 2.5, gde_y - a * 6),
                                 (gde_x - a * 5, gde_y - a * 3.5)),
                                color_2)
            if randint(0, 1):
                self.drawer.rectangle(((gde_x - a * 3.25, gde_y - a * 2.5), (gde_x - a * 1.75, gde_y)), color_3)
            else:
                self.drawer.rectangle(
                    ((gde_x - a * 3.25, gde_y - a * 2.75), (gde_x - a * 1.75, gde_y - a * 1.25)),
                    color_4)

    def make_sun(self, gde_y, color='#ffff1c'):
        if self.checkBox_sun.checkState():
            gde_x = randint(250, 1000)
            a = 20
            self.drawer.ellipse(((gde_x - a * 2, gde_y - a * 2), (gde_x, gde_y)), color)

    def make_path(self, gde_y, color='#b89628', color_2='#695515'):
        if self.checkBox_path.checkState():
            gde_x = randint(100, 1000)
            if gde_y >= 500:
                a = 55
            elif gde_y >= 370:
                a = 30
            elif gde_y >= 200:
                a = 15
            if randint(0, 1):
                self.drawer.rectangle(((gde_x - a, self.delenie), (gde_x, 750)), color)
                self.drawer.rectangle(((gde_x - a * 0.1, self.delenie), (gde_x, 750)), color_2)
                self.drawer.rectangle(((gde_x - a * 0.9, self.delenie), (gde_x - a, 750)), color_2)
            else:
                self.drawer.rectangle(((0, gde_y + a), (1000, gde_y)), color_2)
                self.drawer.rectangle(((0, gde_y + a * 0.9), (1000, gde_y)), color)
                self.drawer.rectangle(((0, gde_y + a * 0.1), (1000, gde_y)), color_2)

    def make_mount(self, gde_y, color='#e88a25', color_2='#6e3c0b'):
        if self.mount.checkState():
            gde_x = randint(290, 1000)
            if gde_y >= 500:
                a = 40
            elif gde_y >= 370:
                a = 30
            elif gde_y >= 200:
                a = 20

            # gde_y = self.delenie
            self.drawer.polygon(((gde_x, gde_y),
                                 (gde_x - a * 5, gde_y - a * 3),
                                 (gde_x - a * 8, gde_y)),
                                color)
            self.drawer.polygon(((gde_x, gde_y),
                                 (gde_x - a * 4, gde_y - a * 2.4),
                                 (gde_x - a * 8, gde_y)),
                                color_2)

    def make_season(self):
        if self.season.isChecked():
            if self.radioButton_now_season.isChecked():
                b = (datetime.datetime.now().month + 1) % 12
                if b == 0:
                    b = 9
                a = str(b // 3 + 2)
                print(a)
                self.season_id = a
            else:
                for season in self.spin_season.keys():
                    if season.isChecked():
                        self.season_id = self.spin_season[season]
                        # print(self.spin_season[season])

    def make_time(self):
        if self.time.isChecked():
            if self.radioButton_now.isChecked():
                a = str(datetime.datetime.now().hour // 6 + 2)
                print(a)
                if a == '2':
                    a = '5'
                self.day_id = a
            else:
                for day in self.spin_day.keys():
                    if day.isChecked():
                        self.day_id = (self.spin_day[day])
                        # print(self.spin_day[day])

    def make_lighthouse(self, gde_y, color='#ffffff', color_2='#ff0000', color_3='#664910', color_4='#000000'):
        color = self.db(7)
        color_2 = self.db(3)
        color_3 = self.db(2)
        if self.checkBox_lighthouse.checkState():
            gde_x = randint(200, 1000)
            if gde_y >= 500:
                a = 40
            elif gde_y >= 370:
                a = 25
            elif gde_y >= 200:
                a = 15
            self.drawer.rectangle(((gde_x - a * 3, gde_y - a * 0.5), (gde_x + a, gde_y)), color_3)

            self.drawer.rectangle(((gde_x - a * 2, gde_y - a * 6.5), (gde_x, gde_y - a * 5.5)), color)
            self.drawer.rectangle(((gde_x - a * 2, gde_y - a * 5.5), (gde_x, gde_y - a * 4.5)), color_2)
            self.drawer.rectangle(((gde_x - a * 2, gde_y - a * 4.5), (gde_x, gde_y - a * 3.5)), color)
            self.drawer.rectangle(((gde_x - a * 2, gde_y - a * 3.5), (gde_x, gde_y - a * 2.5)), color_2)
            self.drawer.rectangle(((gde_x - a * 2, gde_y - a * 2.5), (gde_x, gde_y - a * 1.5)), color)
            self.drawer.rectangle(((gde_x - a * 2, gde_y - a * 1.5), (gde_x, gde_y - a * 0.5)), color_2)

            self.drawer.chord(xy=(gde_x - a * 2.33, gde_y - a * 8, gde_x + a * 0.33, gde_y - a * 5),
                              start=180, end=0, fill=color_4)

    def make_fence(self, gde_y, color='#5c4007'):
        color = self.db(1)
        if self.checkBox_fence.checkState():
            gde_x = randint(300, 1000)
            if gde_y >= 500:
                a = 27
            elif gde_y >= 370:
                a = 15
            elif gde_y >= 200:
                a = 8
            for i in range(self.spinBox_fence.value()):
                self.drawer.rectangle(((gde_x - (a * (i * 2 + 1)), gde_y - a * 5), (gde_x - a * i * 2, gde_y)),
                                      color)
            self.drawer.rectangle(((gde_x - (a * (i * 2 + 1)), gde_y - a * 4), (gde_x, gde_y - a * 3)),
                                  color)
            self.drawer.rectangle(((gde_x - (a * (i * 2 + 1)), gde_y - a * 2), (gde_x, gde_y - a)),
                                  color)

    def make_animals(self, gde_y, color='#70510d', color_2='#000000', color_3='#916810'):
        if self.checkBox_animals.checkState():
            color = self.db(19, season=True)
            color_3 = self.db(20, season=True)
            gde_x = randint(200, 1000)
            if gde_y >= 500:
                a = 50
            elif gde_y >= 350:
                a = 30
            elif gde_y >= 200:
                a = 23
            if randint(0, 1):
                self.drawer.ellipse(((gde_x - a * 2.33, gde_y - a), (gde_x, gde_y + a * 0.2)), color)
                self.drawer.line(
                    xy=(
                        (gde_x - a * 0.6, gde_y - a * 0.5),
                        (gde_x - a * 0.6, gde_y + a * 0.7),
                        (gde_x - a * 0.3, gde_y + a * 0.7)
                    ), fill=color, width=7)
                self.drawer.line(
                    xy=(
                        (gde_x - a * 1.8, gde_y - a * 0.5),
                        (gde_x - a * 1.8, gde_y + a * 0.7),
                        (gde_x - a * 1.5, gde_y + a * 0.7)
                    ), fill=color, width=7)
                self.drawer.ellipse(((gde_x - a * 0.65, gde_y - a * 1.33), (gde_x + a * 0.15, gde_y - a * 0.5)),
                                    color_3)
                self.drawer.polygon(((gde_x - a * 0.65, gde_y - a),
                                     (gde_x + a * 0.1, gde_y - a * 1.4),
                                     (gde_x + a * 0.14, gde_y - a)),
                                    color_3)
                self.drawer.polygon(((gde_x - a * 0.65, gde_y - a),
                                     (gde_x - a * 0.6, gde_y - a * 1.4),
                                     (gde_x + a * 0.14, gde_y - a)),
                                    color_3)
                self.drawer.ellipse(((gde_x - a * 0.55, gde_y - a * 1.15), (gde_x - a * 0.34, gde_y - a * 1)),
                                    color_2)
                self.drawer.ellipse(((gde_x - a * 0.17, gde_y - a * 1.15), (gde_x + a * 0.08, gde_y - a * 1)),
                                    color_2)
            else:
                self.drawer.chord(xy=(gde_x - a * 2.33, gde_y - a, gde_x, gde_y + a),
                                  start=180, end=0, fill=color)
                self.drawer.line(
                    xy=(
                        (gde_x - a * 0.6, gde_y - a * 0.2),
                        (gde_x - a * 0.6, gde_y + a * 0.4),
                        (gde_x - a * 0.3, gde_y + a * 0.4)
                    ), fill=color, width=3)
                self.drawer.line(
                    xy=(
                        (gde_x - a * 1.8, gde_y - a * 0.2),
                        (gde_x - a * 1.8, gde_y + a * 0.4),
                        (gde_x - a * 1.5, gde_y + a * 0.4)
                    ), fill=color, width=3)
                self.drawer.ellipse(((gde_x - a * 0.75, gde_y - a * 0.6), (gde_x - a * 0.4, gde_y - a * 0.25)), color_2)

    def make_fish(self, gde_y, color='#2130d1', color_2='#000000'):
        color = self.db(12)
        if self.checkBox_fish.checkState():
            gde_x = randint(200, 1000)
            if gde_y >= 500:
                a = 40
            elif gde_y >= 370:
                a = 25
            elif gde_y >= 200:
                a = 15
            self.drawer.chord(xy=(gde_x - a * 2.33, gde_y - a, gde_x, gde_y + a),
                              start=180, end=0, fill=color)
            self.drawer.ellipse(((gde_x - a, gde_y - a * 0.5), (gde_x - a * 0.5, gde_y)), color_2)
            self.drawer.polygon(((gde_x - a * 2.33, gde_y),
                                 (gde_x - a * 3.33, gde_y - a),
                                 (gde_x - a * 3.33, gde_y)),
                                color)

    def make_boat(self, gde_y, color='#805216', color_2='#ffffff'):
        if self.checkBox_boat.checkState():
            color_2 = self.db(7)
            color = self.db(1)
            gde_x = randint(290, 1000)
            if gde_y >= 500:
                a = 27
            elif gde_y >= 370:
                a = 15
            elif gde_y >= 200:
                a = 10

            self.drawer.polygon(((gde_x - a, gde_y),
                                 (gde_x - a * 4, gde_y),
                                 (gde_x - a * 5, gde_y - a * 2),
                                 (gde_x, gde_y - a * 2)),
                                color)
            self.drawer.rectangle(((gde_x - a * 2.2, gde_y), (gde_x - a * 2.5, gde_y - a * 5)), color)

            self.drawer.polygon(((gde_x - a * 2.2, gde_y - a * 5),
                                 (gde_x - a * 0.8, gde_y - a * 3.75),
                                 (gde_x - a * 2.2, gde_y - a * 2.5)),
                                color_2)

    def make_draw(self):
        """" Основная функция, которая начинает создания изображения по заданным данным"""

        self.spinbox = {self.tree: 'self.spinBox_tree.value()', self.checkBox_boat: 'self.spinBox_boat.value()',
                        self.checkBox_house: 'self.spinBox_house.value()',
                        self.checkBox_animals: 'self.spinBox_animals.value()',
                        self.checkBox_fish: 'self.spinBox_fish.value()',
                        self.checkBox_fence: '1',
                        self.checkBox_lighthouse: 'self.spinBox_lighthouse.value()'
                        }  # Словарь чтобы задать колличество элементов на картинке

        self.con = sqlite3.connect("PYQT_Project_db.db")
        # Создание курсора
        self.cur = self.con.cursor()
        self.day_id = '3'
        self.season_id = '4'
        self.width = 1000
        self.height = 750
        self.im = Image.new("RGB", (self.width, self.height), (35, 237, 247))
        self.drawer = ImageDraw.Draw(self.im)
        self.elementer()  # Создаём список что будет входить в наш рисунок
        if self.element <= 5:
            self.delenie = 500
        elif self.element <= 12:
            self.delenie = 350
        else:
            self.delenie = 200

        self.make_time()  # Устанавливаем время и погоду
        self.make_season()
        self.color_back = self.db(13, day=True)
        if self.color_down == '#2663de':
            self.color_down1 = self.db(6, day=True)
        elif self.color_down == '#7bd444':
            self.color_down1 = self.db(5, season=True, day=True)
        else:
            self.color_down1 = self.db(16, day=True, season=True)
        self.drawer.rectangle(((0, 0), (1000, self.delenie)), self.color_back)
        self.drawer.rectangle(((0, self.delenie), (1000, 750)), self.color_down1)

        self.make_sun(randint(75, self.delenie - 100), color=self.db(14))  # Добавляем солнце

        if self.checkBox_cloud.isChecked():
            result = self.db(9)
            for i in range(self.spinBox_cloud.value()):  # Рисуем облака на заднем фоне " ORDER BY RAND() LIMIT 1"
                self.make_cloud(randint(150, self.delenie), color=result)

        self.count = 0
        if self.mount.isChecked():  # При большом колличестве элементов мы рисуем деревья на фоне
            gde_y = self.delenie
            result_brown = self.db(2)
            result_orange = self.db(8)
            for i in range(self.spinBox_mount.value()):
                self.make_mount(gde_y, color=result_brown, color_2=result_orange)

        if self.checkBox_path.isChecked():  # Добавляем тропинку
            result_brown = self.db(1)
            result_light_brown = self.db(2)
            for i in range(self.spinBox_path.value()):
                gde_y = randint(self.delenie, 750)
                self.make_path(gde_y, color=result_brown, color_2=result_light_brown)

        if self.radioButton_ocean.isChecked() and self.checkBox_house.isChecked():  # Если мы рисуем океан то дома ррисуются в дали
            for i in range(self.spinBox_house.value()):
                self.make_house(self.delenie)
            self.element -= self.spinBox_house.value()
            self.spisok_element.remove(self.checkBox_house)

        if self.radioButton_forest.isChecked() and self.tree.isChecked():  # Вначале рисуем фон из деревьев, если это лес
            gde_y = randint(self.delenie, 250)
            for i in range(self.spinBox_tree.value()):
                if randint(0, self.spinBox_tree.value() // 4):
                    self.make_tree(gde_y)
                else:
                    gde_y = randint(gde_y, 380)
                    self.count += 1
            self.element -= self.spinBox_tree.value()
            self.spinbox[self.tree] = 'self.count'
            self.element += self.count  # убераем из колличества элементов число деревьев

        self.spisok_gde_y = []
        for w in range(self.element):  # создаём значения по у чтобы рисовать объекты от дальнего к ближайшему
            self.spisok_gde_y.append(randint(self.delenie, 750))

        self.spisok_gde_y.sort()

        for j in range(
                len(self.spisok_gde_y)):  # Мы вызываем функции рисования, убирая если значение сколько осталось ровняется нулю
            el = choice(self.spisok_element)
            self.spinbox[el] = self.spinbox[el] + '-1'
            print(eval(self.spinbox[el]))
            eval(f'{self.sl[el]}({self.spisok_gde_y[j]})')
            if eval(self.spinbox[el]) == 0:
                self.spisok_element.remove(el)
                print('end')

        try:
            name = self.filename.toPlainText()
            self.est = False
            with open('Name_text.txt', mode='r', encoding="utf8") as file:
                for line in file:
                    if name in line:
                        self.est = True
                file.close()
            if not self.est:
                with open('Name_text.txt', mode='w', encoding="utf8") as file:
                    file.write(name)
                    file.close()
            else:
                name = self.run()
                with open('Name_text.txt', mode='w', encoding="utf8") as file:
                    file.write(name)
                    file.close()
            self.im.save(name)
            self.second_form = Second_form(name)
            self.second_form.show()
        except Exception:
           self.label_2.setText('Нужно с .png')
        self.con.close()

    def elementer(self):
        ''' В этой функции мы создаём список всех элементов, которые будут входить в рисунок, а также колличество элементов '''

        self.spisok_element = []
        self.element = 0

        for elem in self.spinbox.keys():  # Проверяем какие кнопки включенны из чего записываем список чего включаем в рисунок
            if elem.checkState():
                self.spisok_element.append(elem)

        for elems in self.spisok_element:  # Записываем колличество предметов
            a = eval(self.spinbox[elems])
            self.element += a

    def run(self):
        name, ok_pressed = QInputDialog.getText(self, "У вас есть картинка с таким названием",
                                                "Введите новое название")
        if ok_pressed:
            return name

    def restart(self):
        ''' Функция, которая отвечает за перезапуск выбора между основой рисунка(океаном, лесом и поляной)'''
        radioButton = self.sender()
        if radioButton.isChecked():
            for elems in self.restart_new[radioButton]:
                eval(elems)
        self.color_down = self.down[radioButton]

    def spin_check(self):
        ''' Функция работы кнопок'''
        for elem in self.spin[self.sender()]:
            if self.sender().checkState():
                elem.setEnabled(True)
                self.i += 6
            else:
                elem.setEnabled(False)
                self.i -= 6
            self.progressBar.setValue(self.i)

    def spin_sun(self):
        if self.sender().checkState():
            self.i += 6
        else:
            self.i -= 6
        self.progressBar.setValue(self.i)

    def color_change(self):
        if self.sender().checkState():
            self.color_roof = QColorDialog.getColor()
            if self.color_roof.isValid():
                self.sender().setStyleSheet(
                    "background-color: {}".format(self.color_roof.name()))

    def db(self, number, season=False, day=False):
        try:
            if season:  # Проверяем важен ли нам сезон года, или время дня
                if not day:
                    a = self.cur.execute(
                        "SELECT cod, day FROM color_main WHERE color = " + str(
                            number) + " and (season = " + self.season_id + ")").fetchall()
                    result1, b = choice(a)
                    return result1
                else:
                    a = self.cur.execute(
                        "SELECT cod, day FROM color_main WHERE color = " + str(
                            number) + " and (day = " + self.day_id
                        + ")" + " and (season = " + self.season_id + ")").fetchall()
                    result1, b = choice(a)
                    return result1
            else:
                a = self.cur.execute(
                    "SELECT cod, day FROM color_main WHERE color = " + str(number) + " and (day = " + self.day_id
                    + ")").fetchall()
                result1, b = choice(a)
                return result1
        except Exception:
            return '#000000'


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Draw_maker()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
