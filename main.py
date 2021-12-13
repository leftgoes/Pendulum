import math
import time
import ctypes
import pyautogui
import os
from PIL import Image, ImageDraw
import win32api, win32gui

from objects import Vector


class Pendulum:
    def __init__(self, r, theta0=0.0, v0=0.0, k=0.0):
        self.r = r
        self.theta = theta0
        self.v = v0
        self.k = k
        self.g = 9.81

    def __repr__(self):
        return f'Pendulum({self.r}, {self.theta})'

    def gravity(self, delta_t):
        a = -self.g * math.sin(self.theta) / self.r
        self.v += a * delta_t - self.k * self.v
        self.theta += self.v/self.r * delta_t

    @property
    def x(self):
        return -self.r * math.cos(self.theta + math.pi/2)

    @property
    def y(self):
        return self.r * math.sin(self.theta + math.pi/2)

    @property
    def position(self):
        return Vector(self.x, self.y)


class Simulate:
    def __init__(self):
        self.do = True
        self.size = pyautogui.size()
        # self.size = (1800, 900)
        self.origin = Vector(int(self.size[0] / 2), int(self.size[1] / 2) - 50)
        self.img, self.draw = None, None
        self.r = 30
        pass

    def simulate(self, key, n=10, delta_t=.008, directory='C:\\Python\\Pendulum\\__pycache__\\__temp__', **kwargs):
        for f in os.listdir(directory):
            if f.endswith(".png"):
                os.remove(os.path.join(directory, f))

        os.chdir(directory)
        pendulum = Pendulum(400, 2, **kwargs)
        while True:  # while True
            for i in range(n):
                for _ in range(15):
                    if win32api.GetKeyState(key) < 0:
                        offset = Vector(win32gui.GetCursorPos()) - (pendulum.position + self.origin)
                        if offset.r < self.r:
                            pendulum.v = v = 0
                            pressed, theta_before = True, 0
                            while pressed:
                                for j in range(n, 2*n):
                                    if 0 <= win32api.GetKeyState(key):
                                        pressed = False
                                        break
                                    else:
                                        v, theta_before = (pendulum.theta - theta_before)/(n*delta_t), pendulum.theta
                                        pendulum.theta = -(Vector(win32gui.GetCursorPos()) - offset - self.origin).theta + math.pi/2
                                        self.draw_pendulum(pendulum)
                                        self.img.save(f'__temp__{j}.png')
                                        self.set_wallpaper(f'{directory}\\__temp__{j}.png')
                                        time.sleep(delta_t)
                            pendulum.v = v
                        pendulum.gravity(1)
                    else:
                        pendulum.gravity(1)
                self.draw_pendulum(pendulum)
                self.img.save(f'__temp__{i}.png')
                self.set_wallpaper(f'{directory}\\__temp__{i}.png')
                time.sleep(delta_t)

    def new_canvas(self):
        self.img = Image.new('RGB', self.size, (0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)

    def draw_pendulum(self, pendulum, color=(255, 255, 255), **kwargs):
        self.new_canvas()
        p = pendulum.position + self.origin
        origin = 5
        self.draw.line((*self.origin, p.x, p.y), fill=color, width=3, **kwargs)
        self.draw.ellipse((self.origin[0] - origin, self.origin[1] - origin, self.origin[0] + origin, self.origin[1] + origin), fill=(0, 150, 255))
        self.draw.ellipse((p.x - self.r, p.y - self.r, p.x + self.r, p.y + self.r), fill=(130, 190, 255), outline=(0, 150, 255), width=5)

    def set_wallpaper(self, path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
