from importlib.util import set_loader
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
import glm  # Make sure glm is imported for matrix manipulations

class Camera:
    def __init__(self, width, height, initalPos=[0.0,0.0,4.0],initalFront=[0.0,0.0,-2.0], initialUp=[0.0,1.0,0.0], bgColor =[0.1,0.0,0.0] ):
        self.width = width
        self.height = height
        self.pos = np.array(initalPos, dtype=np.float32)  # Camera position
        self.front = np.array(initalFront, dtype=np.float32)  # Camera looking direction
        self.up = np.array(initialUp, dtype=np.float32)  # Up direction
        self.bgColor = bgColor


        self.scroll_speed = 0.1
        self.speed = 0.005
        self.pitch = 0.0  # Vertical angle
        self.yaw = -90.0  # Horizontal angle
        self.mouse_sensitivity = 0.01  # Mouse sensitivity

    def get_projection(self):
        return glm.perspective(glm.radians(45.0), self.width / self.height, 0.1, 100.0)
    
    def get_view(self):
        return glm.lookAt(glm.vec3(*self.pos), glm.vec3(*(self.pos + self.front)), glm.vec3(*self.up))
    
    def zoom(self, z):
        # Adjust the camera's Z position to zoom in and out
        self.pos += self.scroll_speed * self.front * z

    def process_inputs(self, keys, mouse_dx, mouse_dy):
        # Camera movement controls
        if keys[pg.K_w]:
            self.pos += self.front * self.speed
        if keys[pg.K_s]:
            self.pos -= self.front * self.speed
        if keys[pg.K_q]:
            self.pos += self.up * self.speed
        if keys[pg.K_e]:
            self.pos -= self.up * self.speed
        if keys[pg.K_a]:
            self.pos -= np.cross(self.front, self.up) * self.speed
        if keys[pg.K_d]:
            self.pos += np.cross(self.front, self.up) * self.speed

        # Camera rotation with mouse movement
        self.yaw += mouse_dx * self.mouse_sensitivity
        self.pitch += mouse_dy * self.mouse_sensitivity

        # Clamping the pitch to avoid flipping
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        # Calculate the front vector based on yaw and pitch
        direction = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
        ])

        self.front = direction / np.linalg.norm(direction)

