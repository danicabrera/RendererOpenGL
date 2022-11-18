from pickle import *
import pygame
from pygame.locals import *

from shaders import *

from gl import Renderer, Model
from math import cos, sin, radians, tan

width = 960
height = 540

deltaTime = 0.0

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(vertex_shader, fragment_colors)

rend.target.z = -5
#mug
#Penguin
#Sword
#tree
#rose
face = Model("Penguin.obj", "Model.bmp")

face.position.z -= 5
face.position.y -= 1
face.scale.x = 0.25
face.scale.y = 0.25
face.scale.z = 0.25

rend.scene.append( face )
value = 1
modelo = 1

isRunning = True

while isRunning:

    keys = pygame.key.get_pressed()
    mouse_position = pygame.mouse.get_pos()


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
            elif event.key == pygame.K_c:
                if value == 1:
                    rend.setShaders(vertex_shader, fragment_shader)
                    value = 2
                elif value == 2:
                    rend.setShaders(vertex_shader, fragment_toon_shader)
                    value = 3
                elif value == 3:
                    rend.setShaders(vertex_shader, fragment_glow)
                    value = 4
                elif value == 4:
                    rend.setShaders(vertex_shader, fragment_colors)
                    value = 1



    if keys[K_a]:
        rend.angle -= 30 * deltaTime
    elif keys[K_d]:
        rend.angle += 30 * deltaTime


    if keys[K_q]:
        if rend.camDistance > 2:
            rend.camDistance -= 2 * deltaTime

    elif keys[K_e]:
        if rend.camDistance < 5:
            rend.camDistance += 2 * deltaTime

    if keys[K_w]:
        rend.camPosition.y += 10 * deltaTime

    elif keys[K_s]:
        rend.camPosition.y -= 10 * deltaTime

    rend.camPosition.x = rend.target.x + sin(radians(rend.angle)) * rend.camDistance
    rend.camPosition.z = rend.target.z + cos(radians(rend.angle)) * rend.camDistance

    rend.target.y = rend.camPosition.y

    if keys[K_LEFT]:
        rend.pointLight.x -= 10 * deltaTime

    elif keys[K_RIGHT]:
        rend.pointLight.x += 10 * deltaTime

    elif keys[K_UP]:
        rend.pointLight.y += 10 * deltaTime

    elif keys[K_DOWN]:
        rend.pointLight.y -= 10 * deltaTime

        # Modelos
    elif keys[K_m]:
        if modelo == 1:
            rend.scene.clear()
            face = Model("Penguin.obj", "Penguin.bmp")
            face.position.z -= 5
            face.position.y -= 1
            face.scale.x = 0.25
            face.scale.y = 0.25
            face.scale.z = 0.25
            rend.scene.append(face)

            modelo = 2

        elif modelo == 2:
            rend.scene.clear()
            face = Model("rose.obj", "Model.bmp")
            face.position.z -= 5
            face.position.y -= 1
            face.scale.x = 0.25
            face.scale.y = 0.25
            face.scale.z = 0.25
            rend.scene.append(face)

            modelo = 3

        elif modelo == 3:
            rend.scene.clear()
            face = Model("mug.obj", "Model.bmp")
            face.position.z -= 5
            face.position.y -= 1
            face.scale.x = 0.25
            face.scale.y = 0.25
            face.scale.z = 0.25
            rend.scene.append(face)

            modelo = 4
        elif modelo == 4:
            rend.scene.clear()
            face = Model("Sword.obj", "Model.bmp")
            face.position.z -= 5
            face.position.y -= 1
            face.scale.x = 0.25
            face.scale.y = 0.25
            face.scale.z = 0.25
            rend.scene.append(face)

            modelo = 5
        elif modelo == 5:
            rend.scene.clear()
            face = Model("tree.obj", "Model.bmp")
            face.position.z -= 5
            face.position.y -= 1
            face.scale.x = 0.25
            face.scale.y = 0.25
            face.scale.z = 0.25
            rend.scene.append(face)

            modelo = 1

    deltaTime = clock.tick(60) / 1000

    rend.Time += deltaTime

    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()