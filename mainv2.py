import pygame as pg
import pymunk
import pymunk.pygame_util
import random
pymunk.pygame_util.positive_y_is_up = False
from pymunk import Vec2d
import math
RES = WIDTH, HEIGHT = 1200, 900
FPS = 100
collision_types = {
    "ball": 1,
    "brick": 2,
    "bottom": 3,
    "player": 4,
}
pg.init()
surface = pg.display.set_mode(RES)

clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

#настройки pymunk
space = pymunk.Space()
space.gravity = 0, 0
static_body = space.static_body
#создание ограничивающих линий
for el in [[(1, HEIGHT), (WIDTH, HEIGHT)], [(1, 1), (1, HEIGHT)], [(WIDTH, 1), (WIDTH, HEIGHT)], [(WIDTH, 1), (0, 0)]]:
    segment_shape = pymunk.Segment(space.static_body, el[0], el[1], 2)
    segment_shape.elasticity = 0.4
    segment_shape.friction = 1.0
    space.add(segment_shape)
#создание лужи
# segment_shape = pymunk.Segment(space.static_body, (0, 0), (100, 100), 100)
# space.add(segment_shape)

#Создание объектов

def create_ball(space, pos, direction):
    density = 6000
    ball_radius = random.randrange(30, 100) #радиус
    ball_mass = density * 3.14 * ball_radius ** 2 * 0.04
    velocity = random.randrange(300, 500)
    
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius) #момент инерции

    ball_body = pymunk.Body(ball_mass, ball_moment) #экземпляр тела
    ball_body.position = pos
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.8
    ball_shape.friction = 1.0
    ball_shape.color = [random.randrange(256) for i in range(4)]
    ball_shape.collision_type = collision_types["ball"]
    ball_body.apply_impulse_at_local_point(Vec2d(*direction))

    def constant_velocity(body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * velocity

    ball_body.velocity_func = constant_velocity

    pivot = pymunk.PivotJoint(static_body, ball_body, (0, 0), (0, 0))
    pivot.max_bias = 0
    pivot.max_force = 1000000
    space.add(ball_body, ball_shape, pivot)
    return [ball_body, ball_radius, ball_body.velocity[0], ball_body.velocity[1]]

balls = [create_ball(space, 
(random.randrange(100, WIDTH - 100), 
random.randrange(100, HEIGHT - 100)), 
random.choice([(1, 10), (-1, 10)])) for i in range(random.randrange(1, 20))]
space.add(pymunk.Circle(space.static_body, 3))
color = (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))
time = 0
while True:
    time = (time + 1) % 10
    surface.fill(pg.Color('black'))

    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
    for elem in balls:
        obj = elem[0]
        x, y = obj.position
        
        d = ((600 - x) ** 2 + (600 - y) ** 2) ** 0.5
        
        # if d <= 200 + elem[1]:
        #     vx, vy = obj.velocity[0], obj.velocity[1]
        #     if time == 9:
        #         ab = 50
        #         if vx > 0: vx = max(0, vx - ab)
        #         else: vx = min(0, vx + ab)
        #         if vy > 0: vy = max(0, vy - ab)
        #         else: vy = min(0, vy + ab)
        #         print(obj.velocity)
            
        #         elem[2] -= 1
        #         elem[3] -= 1
        #         if obj.velocity[0] > 0: vx = max(0, obj.velocity[0] - ab)
        #         else: vx = min(0, obj.velocity[0] + ab); print("СКА")
        #         if obj.velocity[1] > 0: vy = max(0, obj.velocity[1] - ab)
        #         else: vy = min(0, obj.velocity[1] + ab); print("ЗАЕБАЛ БЛЯЬБ")
        #         obj.velocity = (vx, vy)
        #         print(obj.velocity)

    pg.draw.circle(surface, color, 
                    (600, 600), 200)
    space.step(1 / FPS)
    space.debug_draw(draw_options)
    pg.display.flip()
    clock.tick(FPS)