import tkinter as tk
from PIL import Image, ImageTk
from time import time, sleep
from random import choice, uniform, randint
from particle import Particle


# 颜色选项
colors = ['red', 'blue', 'yellow', 'white', 'green', 'orange', 'purple', 'seagreen', 'indigo', 'cornflowerblue']
HEIGHT = 800
WIDTH = 1200


def simulate(cv):
    """
        循环调用保持不停
    """
    t = time()
    explode_points = []
    wait_time = randint(10, 100)
    numb_explode = randint(5, 50)
    # 创建一个所有粒子同时扩大的二维列表
    for point in range(numb_explode):
        objects = []
        x_cordi = randint(0.05 * WIDTH, 0.95 * WIDTH)
        y_cordi = randint(0.05 * HEIGHT, 0.95 * HEIGHT)
        speed = uniform(0.2, 2.)
        size = uniform(0.2, 3)
        color = choice(colors)
        explosion_speed = uniform(0.1, 0.5)
        explosion_radius = randint(5, 15)
        total_particles = randint(20, 50)
        for i in range(1, total_particles):
            r = Particle(cv, idx=i, total=total_particles, explosion_speed=explosion_speed, explosion_radius=explosion_radius,
                         x=x_cordi, y=y_cordi, vx=speed, vy=speed, color=color, size=size, lifespan=abs(uniform(0.2, 1.75)))
            objects.append(r)
        explode_points.append(objects)

    total_time = .0
    # 1.8s内一直扩大
    while total_time < 1.8:
        sleep(0.01)
        tnew = time()
        t, dt = tnew, tnew - t
        for point in explode_points:
            for item in point:
                item.update(dt)
        cv.update()
        total_time += dt
    # 循环调用
    root.after(wait_time, simulate, cv)


def close(*ignore):
    """退出程序、关闭窗口"""
    global root
    root.quit()


if __name__ == '__main__':
    root = tk.Tk()
    cv = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    # 选一个好看的背景会让效果更惊艳！
    image = Image.open("./background.jpg")
    photo = ImageTk.PhotoImage(image)

    cv.create_image(0, 0, image=photo, anchor='nw')
    cv.pack()

    root.protocol("WM_DELETE_WINDOW", close)
    root.after(100, simulate, cv)
    root.mainloop()


