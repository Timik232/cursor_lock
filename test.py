import sys
import keyboard
import pyautogui
import win32api
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt, QTimer
import time

import PyQt5.QtGui
import PyQt5.QtCore

screen_size = pyautogui.size()
xMin = 0
yMin = 0
monitor_info = win32api.GetMonitorInfo(win32api.EnumDisplayMonitors()[0][0])
monitor_left, monitor_top, monitor_right, monitor_bottom = monitor_info.get("Monitor")
x_min, y_min = monitor_left+2, monitor_top-2
x_max, y_max = monitor_right-2, monitor_bottom+2
running = False


class CursorBlocker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.block_cursor)



    def closeEvent(self, event,action=False):
        if not action:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                'Cursor Blocker',
                'The application is still running. To exit, right-click this icon and choose "Exit".',
                QSystemTrayIcon.Information,
                5000
            )
        else:
            self.tray_icon.setVisible(False)
            exit()


    def initUI(self):
        self.setWindowTitle("Cursor Blocker")
        # Создаем кнопки и метки для отображения статуса
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_block)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_block)
        self.stop_button.setEnabled(False)
        self.label = QLabel("Cursor unblocked.", self)
        self.tint = QLabel("Press shift + L to toggle block", self)

        # Размещаем элементы на форме
        self.start_button.move(50, 50)
        self.stop_button.move(150, 50)
        self.label.move(50, 100)
        self.tint.move(50,20)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.ico'))
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip('Cursor Blocker')
        self.setWindowIcon(QIcon('icon.ico'))
        # Создаем меню для значка в системном лотке
        menu = QMenu()
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(lambda: self.closeEvent(None, True))
        menu.addAction(exit_action)
        self.tray_icon.setContextMenu(menu)

        self.setGeometry(300, 300, 300, 150)
        self.show()
        # this = self
        # keyboard.add_hotkey('shift+l', this.toggle())

    def start_block(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.label.setText("Cursor blocked.")
        self.timer.start(1)
        # self.block_cursor()

    def stop_block(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.label.setText("Cursor unblocked.")
        self.timer.stop()

    def block_cursor(self):
        x, y = pyautogui.position()
        new_x = x
        new_y = y

        # если курсор находится в пределах экрана, двигать без изменений
        if x_min < x < x_max:
            new_x = x
        elif x <= x_min:
            new_x = x_min
        elif x >= x_max:
            new_x = x_max

        if y_min < y < y_max:
            new_y = y
        elif y <= y_min:
            new_y = y_min
        elif y >= y_max:
            new_y = y_max

        # перемещаем курсор в новые координаты
        win32api.SetCursorPos((new_x, new_y))

    def toggle(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.label.setText("Cursor unblocked.")
        else:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.label.setText("Cursor blocked.")
            self.timer.start(1)

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 38 and event.modifiers() == Qt.ShiftModifier:
            self.toggle()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CursorBlocker()
    sys.exit(app.exec_())
