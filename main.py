import requests
import os
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from UI import Ui_Form

SCREEN_SIZE = [600, 450]


class Map(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.show_map_button.clicked.connect(self.show_map)

    # Вывод изображения карты в зависимости от введённых координат
    def show_map(self):
        self.get_coords()
        self.getImage()

        self.pixmap = QPixmap(self.map_file)
        self.map_label.setPixmap(self.pixmap)

    # Получение введённых пользователем координат и масштаба
    def get_coords(self):
        self.longitude = self.longitude_edit.text().strip()
        self.width = self.width_edit.text().strip()
        self.scale = int(self.scale_edit.text().strip()) * 100

    # Получение изображения по запросу
    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll" \
                      f"={self.longitude},{self.width}8&spn" \
                      f"={1 / self.scale},{1 / self.scale}&l=map"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    map = Map()
    map.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
