import pygame
from pygame.locals import *
import math

pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('3D Cube')
clock = pygame.time.Clock()

vertices = [(-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1),
            (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)]

edges = [(0, 1), (1, 3), (3, 2), (2, 0),
         (4, 5), (5, 7), (7, 6), (6, 4),
         (0, 4), (1, 5), (2, 6), (3, 7)]

camera_pos = [0, 0, -5]
yaw = 0
pitch = 0

fov = 90
aspect_ratio = screen_width / screen_height
near_clip = 1
far_clip = 100

move_speed = 0.1
strafe_speed = 0.1

def project(point):
    x, y, z = point
    x = x * (fov / z) * aspect_ratio
    y = y * (fov / z)
    return (int(x + screen_width / 2), int(y + screen_height / 2))

def transform(vertex):
    x, y, z = vertex
    x -= camera_pos[0]
    y -= camera_pos[1]
    z -= camera_pos[2]
    return (x, y, z)

def rotate_y(point, angle):
    x, y, z = point
    new_x = x * math.cos(angle) + z * math.sin(angle)
    new_z = -x * math.sin(angle) + z * math.cos(angle)
    return (new_x, y, new_z)

def rotate_x(point, angle):
    x, y, z = point
    new_y = y * math.cos(angle) - z * math.sin(angle)
    new_z = y * math.sin(angle) + z * math.cos(angle)
    return (x, new_y, new_z)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        running = False

    if keys[K_LEFT]:
        yaw += 0.03
    if keys[K_RIGHT]:
        yaw -= 0.03
    if keys[K_UP]:
        pitch += 0.03
    if keys[K_DOWN]:
        pitch -= 0.03

    if keys[K_w]:
        camera_pos[0] += math.sin(-yaw) * move_speed
        camera_pos[2] += math.cos(-yaw) * move_speed
    if keys[K_s]:
        camera_pos[0] -= math.sin(-yaw) * move_speed
        camera_pos[2] -= math.cos(-yaw) * move_speed
    if keys[K_a]:
        camera_pos[0] += math.sin(-yaw - math.pi/2) * strafe_speed
        camera_pos[2] += math.cos(-yaw - math.pi/2) * strafe_speed
    if keys[K_d]:
        camera_pos[0] -= math.sin(-yaw - math.pi/2) * strafe_speed
        camera_pos[2] -= math.cos(-yaw - math.pi/2) * strafe_speed

    screen.fill((0, 0, 0))

    rotated_vertices = []
    i = 0
    for vertex in vertices:
        rotated_vertex = vertex
        rotated_vertex = rotate_y(rotated_vertex, yaw)
        rotated_vertex = rotate_x(rotated_vertex, pitch)
        rotated_vertices.append(rotated_vertex)
        i += 1

    for edge in edges:
        start_vertex = rotated_vertices[edge[0]]
        end_vertex = rotated_vertices[edge[1]]

        start_vertex = transform(start_vertex)
        end_vertex = transform(end_vertex)

        start_vertex = project(start_vertex)
        end_vertex = project(end_vertex)

        pygame.draw.line(screen, (255, 255, 255), start_vertex, end_vertex)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
