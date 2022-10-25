import pygame
from pygame.locals import *

from shaders import *

from gl import Renderer, Buffer

width = 960
height = 540

deltaTime = 0.0

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(vertex_shader, fragment_shader)

#           Positions         Colors
triangle = [-0.5, -0.5, 0,    1.0, 0.0, 0.0,
               0,  0.5, 0,    0.0, 1.0, 0.0,
             0.5, -0.5, 0,    0.0, 0.0, 1.0 ]

triangle = Buffer(triangle)
triangle.position.z -= 10

rend.scene.append( triangle )


isRunning = True

while isRunning:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    deltaTime = clock.tick(60) / 1000

    if keys[K_LEFT]:
        rend.camPosition.x -=10 * deltaTime

    if keys[K_RIGHT]:
        rend.camPosition.x +=10 * deltaTime




    #print(deltaTime)

    rend.render()
    pygame.display.flip()

pygame.quit()
