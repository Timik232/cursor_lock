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
        self.monitors = win32api.EnumDisplayMonitors()
        self.max_number = len(self.monitors)
        self.number = 0
        self.active_monitor = self.monitors[self.number]
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

    def show_application(self):
        self.showNormal()

    def initUI(self):
        self.setWindowTitle("Cursor Blocker")
        # Создаем кнопки и метки для отображения статуса
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_block)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_block)
        self.stop_button.setEnabled(False)
        self.label = QLabel("Cursor unblocked.", self)
        self.label_monitor = QLabel(f"Monitor {self.number + 1}", self)
        self.tint = QLabel("Press shift + L to toggle block", self)
        self.tint_change = QLabel("Press shift + ] to change monitor", self)


        # Размещаем элементы на форме
        self.start_button.move(50, 75)
        self.stop_button.move(150, 75)
        self.label.move(50, 110)
        self.tint.move(50, 20)
        self.tint_change.move(50, 50)
        self.label_monitor.move(50, 130)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.ico'))
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip('Cursor Blocker')
        self.setWindowIcon(QIcon('icon.ico'))
        # Создаем меню для значка в системном лотке
        menu = QMenu()
        exit_action = QAction('Exit', self)
        open_action = QAction('Open', self)
        exit_action.triggered.connect(lambda: self.closeEvent(None, True))
        open_action.triggered.connect(self.show_application)
        menu.addAction(open_action)
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
        monitor = self.active_monitor
        left = monitor[2][0]
        top = monitor[2][1]
        right = left + monitor[2][2]
        bottom = top + monitor[2][3]
        win32api.ClipCursor((left, top, right, bottom))

    def toggle(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.label.setText("Cursor unblocked.")
            win32api.ClipCursor((0, 0, 0, 0))
        else:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.label.setText("Cursor blocked.")
            self.timer.start(1)

    def next_monitor(self, flag):
        if flag:
            self.number += 1
        else:
            self.number -= 1
        if self.number >= self.max_number:
            self.number = 0
        if self.number < 0:
            self.number = self.max_number - 1
        self.label_monitor.setText(f"Monitor {self.number + 1}")
        self.active_monitor = self.monitors[self.number]
        if not self.timer.isActive():
            self.timer.stop()
            self.timer.start(1)

    def keyPressEvent(self, event):
        if event.nativeScanCode() == 38 and event.modifiers() == Qt.ShiftModifier:
            self.toggle()
        if event.nativeScanCode() == 27 and event.modifiers() == Qt.ShiftModifier:
            self.next_monitor(True)
        if event.nativeScanCode() == 26 and event.modifiers() == Qt.ShiftModifier:
            self.next_monitor(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CursorBlocker()
    sys.exit(app.exec_())
