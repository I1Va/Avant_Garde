import pygame as pg
import pymunk.pygame_util
import random
pymunk.pygame_util.positive_y_is_up = False
from pymunk import Vec2d

RES = WIDTH, HEIGHT = 1200, 900
FPS = 60

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
space.gravity = 0, 8000
#создание ограничивающих линий
for el in [[(1, HEIGHT), (WIDTH, HEIGHT)], [(1, 1), (1, HEIGHT)], [(WIDTH, 1), (WIDTH, HEIGHT)], [(WIDTH, 1), (0, 0)]]:
    segment_shape = pymunk.Segment(space.static_body, el[0], el[1], 2)
    segment_shape.elasticity = 0.4
    segment_shape.friction = 1.0
    space.add(segment_shape)
#Создание объектов
def spawn_ball(space, position, direction):
    ball_body = pymunk.Body(1, float("inf"))
    ball_body.position = position

    ball_shape = pymunk.Circle(ball_body, 5)
    ball_shape.color = pg.Color("green")
    ball_shape.elasticity = 1.0
    ball_shape.collision_type = collision_types["ball"]

    ball_body.apply_impulse_at_local_point(Vec2d(*direction))

    # Keep ball velocity at a static value
    def constant_velocity(body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * 400

    ball_body.velocity_func = constant_velocity

    space.add(ball_body, ball_shape)

while True:
    surface.fill(pg.Color('black'))

    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                spawn_ball(space, i.pos, random.choice([(1, 10), (-1, 10)]))
                print(i.pos)
    space.step(1 / FPS)
    space.debug_draw(draw_options)
    pg.display.flip()
    clock.tick(FPS)