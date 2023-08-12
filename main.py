import keyboard
import pyautogui
import win32api
import tkinter as tk
import time
import ctypes

screen_size = pyautogui.size()
xMin = 0
yMin = 0
monitor_info = win32api.GetMonitorInfo(win32api.EnumDisplayMonitors()[0][0])
monitor_left, monitor_top, monitor_right, monitor_bottom = monitor_info.get("Monitor")
x_min, y_min = monitor_left+1, monitor_top-1
x_max, y_max = monitor_right-1, monitor_bottom+1
running = True


class CursorBlocker:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.button = tk.Button(root, text="Start", command=self.toggle_block)
        self.button.pack()
        self.monitors = win32api.EnumDisplayMonitors()
        self.active_monitor = self.monitors[0]


        # Создаем метку для отображения статуса
        self.label = tk.Label(root, text="")
        self.label.pack()
        root.bind('<KeyPress-l>', self.start_stop_block)

    def toggle_block(self):
        if self.running:
            # Если блокировка курсора уже запущена, останавливаем ее
            self.running = False
            self.button.config(text="Start")
            self.label.config(text="Cursor unblocked.")
            win32api.ClipCursor((0,0,0,0))
        else:
            # Если блокировка курсора не запущена, запускаем ее
            self.running = True
            self.button.config(text="Stop")
            self.label.config(text="Cursor blocked.")
            self.block_cursor()

    def block_cursor(self):
        monitor = self.active_monitor
        left = monitor[2][0]
        top = monitor[2][1]
        right = left + monitor[2][2]
        bottom = top + monitor[2][3]
        win32api.ClipCursor((left, top, right, bottom))

    def start_stop_block(self, event):
        self.toggle_block()

# Создаем графическое окно
root = tk.Tk()
root.title("Cursor Blocker")

# Создаем экземпляр класса CursorBlocker и запускаем главный цикл обработки событий
app = CursorBlocker(root)
root.mainloop()


