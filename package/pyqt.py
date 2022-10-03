from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800,600)

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        button2 = QPushButton("New button")
        button2.setCheckable(True)
        button2.clicked.connect(self.the_button_was_clicked)


    def the_button_was_clicked(self):
        print("Clicked!")

    def the_button2_was_clicked(self):
        print('afafaf')

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()