import keyboard
import pyautogui
import win32api
import tkinter as tk
import time

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
        else:
            # Если блокировка курсора не запущена, запускаем ее
            self.running = True
            self.button.config(text="Stop")
            self.label.config(text="Cursor blocked.")
            self.block_cursor()

    def block_cursor(self):
        x, y = pyautogui.position()
        if x < x_min:
            x = x_min
        elif x > x_max:
            x = x_max

        if y < y_min:
            y = y_min
        elif y > y_max:
            y = y_max

        win32api.SetCursorPos((x, y))
        if self.running:
            self.root.after(5, self.block_cursor)

    def start_stop_block(self, event):
        self.toggle_block()

# Создаем графическое окно
root = tk.Tk()
root.title("Cursor Blocker")

# Создаем экземпляр класса CursorBlocker и запускаем главный цикл обработки событий
app = CursorBlocker(root)
root.mainloop()


