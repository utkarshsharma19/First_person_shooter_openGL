from sys import displayhook
from turtle import bgcolor
from OpenGL.GL import *
from Camera import Camera
from Light import Light
import pygame as pg
import numpy as np
from Renderer import Renderer
from helpingFunction import *
import Shape as Shape
from Shader import Shader,Gun,Target
from Texture import Texture
from Material import Material
from FrameBuffer import FBO

class GameEngine:
    def __init__(self, display):
        self.display = display
        self.camera = Camera(*display, bgcolor=[.25,.73,0.82])
        staticCamera = Camera(*display, [0,-0.28,-2.5],[0,0,-20], bgcolor=[0,0,0])
        emptyMat = Material()
        light = Light([0,40,20])

        texture = Texture('texture/images (1).jpeg')
        textureGun = Texture('')
        textureTarget= Texture('texture/target.jpg')
        texture_plane = Texture(display = display)

        bright_tex = Material(Type='bright', Texture=texture)
        GunMaterial = Material(Texture=textureGun)
        TargetMaterial = Material(Texture=textureTarget)
        dark = Material(Texture=texture_plane)
        
        shader_light = Shader('Shaders/texVert.glsl','Shaders/texFrag.glsl')
        shader = Shader('Shaders/pulseVert.glsl','Shaders/pulseFrag.glsl')
        defaultShader = Shader('Shaders/defaultVert.glsl','Shaders/defaultFrag.glsl')
        
        VO1 ,F1 = ['in_position', 'in_normal', 'in_tex_coord'], ['3 0', '3 3','2 6']
        VO2, F2 = ['in_tex_coord','in_normal', 'in_position'], ['2 0', '3 2','3 5']
        VO3, F3 = ['in_position', 'in_tex_coord']['2 0', '2 2']

        translateGun = [0,-0.22,3.6]
        GunVertices = getOBJVerticesOriented('', translateGun, 0.005,[0,180,0])
        self.gun = Gun(GunVertices,GunMaterial,shader_light,VO2,F2,translated=translateGun, xpos=5, bulletParams= [emptyMat,defaultShader])

        TargetVertices = getOBJVerticesOriented("",[0,-0.9,-4], rotation=[66,0,0])
        self.target = Target(TargetVertices,TargetMaterial,shader_light,VO2,F2,8)

        self.createMiniCam()

        miniCamScreen = Shape(self.miniCamViewVertices, dark, shader_light, VO3, F3, 4)
        fbo = FBO(texture_plane)

        self.createFloor(50)
        floorTile = Shape(self.floorVertices, bright_tex, shader_light, VO1, F1, 8)
        self.renderer = Renderer([self.gun, floorTile, self.target], self.camera,light,fbo,miniCamScreen, staticCamera )
        glEnable(GL_DEPTH_TEST)
    def start(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.renderer.destroy();
                    pg.quit();
                    quit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button ==4:
                        self.camera.zoom(1)
                    elif event.button ==5:
                        self.camera.zoom(-1)
                    elif event.button==1:
                        self.gun.fire()

            for b in self.gun.bullets:
                b.move()
            self.renderer.render()
                    
            self.renderer.render()
            pg.display.flip()

    
    def createFloor(self,size):
        floorTileVertices = np.array(getCombinedVertices(getFloorTileVertices(), getFloorTileIndices(), [0,1,0]*6,[0,0,1,0,1,1,1,1,0,1,0,0], Index=True))
        floorVertices = floorTileVertices
        mid = size//2
        for i in range(size):
            for j in range(size):
                if i==j and j==mid:
                    continue
            floorVertices = np.concatenate(
                [floorVertices, shiftObjectVertices(floorTileVertices,x=1-mid,z=j-mid)], axis=0
            )
            self.floorVertices = shiftObjectVertices(floorVertices,y=-1)

    def createMiniCam(self):
        miniCamViewVertices = np.array([[-0.98,-0.98,0,0],
        [-0.4,-0.98,1,0],
        [-0.4,-0.4,1,1],
        [-0.4,-0.4,1,1],
        [-0.98,-0.4,0,1],
        [-0.98,-0.98,0,0]])
        self.miniCamViewVertices = shiftObjectVertices(miniCamViewVertices)




        