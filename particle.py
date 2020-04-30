from math import sin, cos, radians
# 模拟重力
GRAVITY = 0.1


class Particle(object):
    def __init__(self, cv, idx, total, explosion_speed, explosion_radius=1, x=0., y=0., vx=0., vy=0., size=2., color='red', lifespan=2):
        """
        粒子在空中随机生成随机，变成一个圈、下坠、消失
        属性:
            - id: 粒子的id
            - x, y: 粒子的坐标
            - vx, vy: 在坐标的变化速度
            - total: 总数
            - age: 粒子存在的时长
            - color: 颜色
            - cv: 画布
            - lifespan: 最高存在时长
        """
        self.id = idx
        self.x = x
        self.y = y
        self.initial_speed = explosion_speed
        self.explosion_radius = explosion_radius
        self.vx = vx
        self.vy = vy
        self.total = total
        self.age = 0
        self.color = color
        self.cv = cv
        self.cid = self.cv.create_oval(
            x - size, y - size, x + size,
            y + size, fill=self.color)
        self.lifespan = lifespan

    def update(self, dt):
        self.age += dt
        # 粒子范围扩大
        if self.alive() and self.expand():
            move_x = cos(radians(self.id * 360 / self.total)) * self.initial_speed
            move_y = sin(radians(self.id * 360 / self.total)) * self.initial_speed
            self.cv.move(self.cid, move_x * self.explosion_radius, move_y * self.explosion_radius)
            self.vx = move_x / (float(dt) * 1000)

        # 以自由落体坠落
        elif self.alive():
            move_x = cos(radians(self.id * 360 / self.total))
            # we technically don't need to update x, y because move will do the job
            self.cv.move(self.cid, self.vx + move_x, self.vy + GRAVITY * dt)
            self.vy += GRAVITY * dt

        # 移除超过最高时长的粒子
        elif self.cid is not None:
            self.cv.delete(self.cid)
            self.cid = None

    # 扩大的时间
    def expand(self):
        return self.age <= 1.2

    # 粒子是否在最高存在时长内
    def alive(self):
        return self.age <= self.lifespan