from pickle import *
import pygame
from pygame.locals import *

from shaders import *

from gl import Renderer, Model

width = 960
height = 540

deltaTime = 0.0

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(vertex_shader, fragment_colors)

rend.target.z = -5

face = Model("Penguin.obj", "Penguin.bmp")

face.position.z -= 5
face.position.y -= 1
face.scale.x = 3
face.scale.y = 3
face.scale.z = 3

rend.scene.append( face )


isRunning = True

while isRunning:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            elif event.key == pygame.K_z:
                rend.filledMode()
            elif event.key == pygame.K_x:
                rend.wireframeMode()


    if keys[K_a]:
        rend.camPosition.x -= 10 * deltaTime

    elif keys[K_d]:
        rend.camPosition.x += 10 * deltaTime

    if keys[K_q]:
        rend.camPosition.z -= 5 * deltaTime

    elif keys[K_e]:
        rend.camPosition.z += 5 * deltaTime

    if keys[K_w]:
        rend.camPosition.y += 10 * deltaTime

    elif keys[K_s]:
        rend.camPosition.y -= 10 * deltaTime


    if keys[K_LEFT]:
        rend.pointLight.x -= 10 * deltaTime

    elif keys[K_RIGHT]:
        rend.pointLight.x += 10 * deltaTime

    elif keys[K_UP]:
        rend.pointLight.y += 10 * deltaTime

    elif keys[K_DOWN]:
        rend.pointLight.y -= 10 * deltaTime

    deltaTime = clock.tick(60) / 1000

    rend.Time += deltaTime

    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()