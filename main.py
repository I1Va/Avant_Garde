import pygame
from random import randrange
from math import sin, cos, sqrt
import os
from PIL import Image
#папка с игровыми данными

# настройка папки ассетов

WIDTH = 1200  # ширина игрового окна
HEIGHT = 800 # высота игрового окна
FPS = 300 # частота кадров в секунду

pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

#Игровой цикл
running = True
color = (179, 123, 207)
green = (82, 223, 146)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
#спрайты


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, vy, vx, Ra, Pl, id):
        self.id = id
        self.vx = vx
        self.vy = vy
        self.R = Ra
        self.m = Pl * Ra ** 2 * 0.04 * 3.14 #масса шайбы в кг
        self.V = sqrt(vx ** 2 + vy ** 2)
        img = Image.open("sourceimg.png")
        width = 2 * Ra
        height = 2 * Ra
        resized_img = img.resize((width, height), Image.ANTIALIAS)
        name = "img\im" + str(Ra) + ".png"
        resized_img.save(name)

        pygame.sprite.Sprite.__init__(self)


      
        player_img = pygame.image.load(name).convert()
        self.image = player_img
        self.image.set_colorkey(WHITE)
        #self.image.fill(green)
        self.rect = self.image.get_rect()
        self.radius = 600
        

        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(HEIGHT - self.rect.width)

    def update(self):
        if self.rect.x + self.R >= WIDTH or self.rect.left <= 0:
            self.vx = - self.vx
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy = -self.vy
            
        dt = 0.1

        for i in all_sprites:
            if i.id != self.id and (i.R + self.R) ** 2 <= (i.rect.x - self.rect.x) ** 2 + (i.rect.y - self.rect.y) ** 2:
               # m1, v0x1, v0y1, a01 = self.m, self.vx, self.vy,     
                i.vx = -i.vx
                i.vy = -i.vy
                self.vx = -self.vx
                self.vy = - self.vy
                
        self.rect.y += self.vy * dt
        self.rect.x += self.vx * dt
all_sprites = pygame.sprite.Group()
for i1 in range(10):
    all_sprites.add(Player(randrange(0, WIDTH), randrange(0, HEIGHT), 10, 10, randrange(20, 40), -1, i1))

#for i in all_sprites:
    #print(i.vx)
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    
    # Рендеринг
    screen.fill(color)
    all_sprites.update()

                
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()