from math import radians
from multiprocessing.context import ForkContext
from turtle import up
import numpy as np
import pygame as pg
from helpingFunction import *
from OpenGL.GL import *
from pyrr import Matrix44
class Shape:
    def __init__(self, vertices, material, shader, FormatAlign = ["in_position"], Format=['3 0'], stride = 3, **kargs):
        self.kargs = kargs
        self.material = material
        self.vertices = vertices
        self.shader = shader
        self.transform = Matrix44.identity(dtype=np.float32)
        self.translated = [0,0,0] if not 'translated' in self.kargs else self.kargs['translated']
        self.scalingFactor = 0.01 if not 'scalingFactor' in self.kargs else self.kargs['scalingFactor']
        self.stride = stride
        self.formatAlign = FormatAlign
        self.Format = Format
        self.vao = None
        self.vbo = None
        self.VertxPos = 0 if not 'xpos' in self.kargs else self.kargs['xpos']
        self.VertyPos = self.VertxPos+1 if not 'ypos' in self.kargs else self.kargs['ypos']
        self.VertzPos = self.VertyPos+1 if not 'zpos' in self.kargs else self.kargs['zpos']
        self.name = 'Shape'
        self.initBuffer()
        

       

       # for i, ele in enumerate(format):
        #    v1 = ele.split()
         #   pos = glGetAttribLocation(self.shader.shader_program, FormatAlign[i])
          #  glVertexAttribPointer(pos, int(v1[0]),GL_FLOAT, GL_FALSE, stride*4, ctypes.c_void_p(int(v1[1])*4))
           # glEnableVertexArrayAttrib(pos)
        
    
    def initBuffer(self):
        self.vao =glGenVertexArrays(1) if not self.vao else self.vao
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1) if not self.vbo else self.vbo
        glBindBuffer(GL_ARRAY_BUFFER, self.vertices.nbytes,self.vertices, GL_STATIC_DRAW)

        for i, ele in enumerate(self.Format):
            vl = ele.split();
            pos = glGetAttribLocation(self.shader.shader_program, self.FormatAlign[i])
            glVertexAttribPointer(pos, int(vl[0]), GL_FLOAT, GL_FALSE, self.stride*4, ctypes.c_void_p(int(vl[1])*4))
            glEnableVertexAttribArray(pos)

    def getModelMatrix(self):
        self.rotate( 0 if not 'rotatex' in self.kargs else radians(self.kargs['rotatex']),
        0 if not 'rotatey' in self.kargs else radians(self.kargs['rotatey']),
        0 if not 'rotatez' in self.kargs else radians(self.kargs['rotatez'])
                        )
        
        self.scale( 1 if not 'scalex' in self.kargs else (self.kargs['scalex']),
            1 if not 'scaley' in self.kargs else (self.kargs['scaley']),
            1 if not 'scalez' in self.kargs else (self.kargs['scalez'])
                        )
        
        self.translate( 0 if not 'translatex' in self.kargs else (self.kargs['translatex']),
            0 if not 'translatey' in self.kargs else (self.kargs['translatey']),
            0 if not 'translatez' in self.kargs else (self.kargs['translatez'])
                        )
        return self.transform
    def translateVert(self, x=0,y=0,z=0):
        self.vertices = np.array(list(map(lambda a: -a, np.array(self.translated))))
        self.initBuffer()

    def rotate(self, x=0, y=0, z=0, rotateMat = None):
        self.transLate(*self.translated)
        self.transform = np.array(rotateMat, dtype=np.float32) if rotateMat!=None else Matrix44.from_eulers([radians(x),radians(y),radians(z)],dtype=np.float32) @self.transform
        self.transLate(*list(map(lambda a: -a, self.translated)))

    def rotateVert(self, x=0,y=0 ,z=0):
        self.translateVert(*self.translated)
        x,y,z = radians(x), radians(y), radians(z)
        combined = self.getRotationMatrix(x,y,z)
        self.vertices =np.array(list(map(lambda a: [*a[:self.VertexPos], *np.dot([a[self.VertxPos],a[self.VertyPos], a[self.VertzPos]], combined)])))
        self.translateVert(*list(map(lambda a: -a, self.translated)))
    def scale(self, x=1, y=1, z=1):
        self.transform = Matrix44.from_scale([x,y,z], dtype=np.float32) @self.transform

    def scaleVert(self,x=0,y=0,z=0):
        self.translateVert(*self.translated)
        x,y,z = radians(x), radians(y), radians(z)
        combined = self.getRotationMatrix(x,y,z)
        self.vertices = np.array(list(map(lambda a: [*a[:self.VertxPos], float(a[self.VertxPos]) * x, float(a[self.VertyPos]) * y, float(a[self.VertzPos]) * z], combined)))
        
    def getRotationMatrix(seld, x, y ,z):
        Rx = np.array([[1,0,0],
                    [0,np.cos(x), -np.sin(x)],
                    [0,-np.sin(x),np.cos(x)]])

        Ry = np.array([[np.cos(y),0,np.sin(y)],
                    [0,1, 0],
                    [np.sin(y),0,np.cos(y)]])


        Rz= np.array([[np.cos(z),-np.sin(x),0],
                [-np.sin(z),np.cos(z),0],
                [0,0,1]])
        combined = np.array(np.dot(Rx, np.dot(Ry, Rz)))
        return combined

    def translate(self, x=0, y=0, z=0):
        self.transform = Matrix44.from_translation([x,y,z], dtype=np.float32) @self.transform

    def getRotateMatrix(self,x,y,z):
        Rx = np.array([[1,0,0],
                    [0,np.cos(x), -np.sin(x)],
                    [0,-np.sin(x),np.cos(x)]])

        Ry = np.array([[np.cos(y),0,np.sin(y)],
                    [0,1, 0],
                    [np.sin(y),0,np.cos(y)]])


        Rz= np.array([[np.cos(z),-np.sin(x),0],
                [np.sin(z),np.cos(z),0],
                [0,0,1]])

    def move(self,keys):
        if 'move' in self.kargs and self.kargs['move']:
            if keys[pg.K_t]:
                self.translate(z=self.speed)
            if keys[pg.K_g]:
                self.translate(z=self.speed)
            if keys[pg.K_f]:
                self.translate(x=self.speed)
            if keys[pg.K_h]:
                self.translate(x=self.speed)
            if keys[pg.K_u]:
                self.scale(1+self.scalingFactor, 1+self.scalingFactor, 1+self.scalingFactor)
            if keys[pg.K_i]:
                self.scale(1-self.scalingFactor, 1-self.scalingFactor, 1-self.scalingFactor)  
    

    def destroy(self):
        self.shader.destroy()
        self.material.destroy()
        glDeleteBuffers(1,[self.vbo])
        glDeleteVertexArrays(1,[self.vbo])
class Gun(Shape):
    def __init__(self, vertices, material, shader, bulletParams, FormatAlign=["in_position"], format=['3 0'], stride=3, pos=[0,0,0], front=[0,0,-1], **kargs):
        super().__init__(vertices, material, shader, FormatAlign, format, stride, **kargs)
        self.speed = 0 if not 'speed' in self.kargs else self.kargs['speed']
        self.mouse_sensitivity = 0.01
        self.bullets = []
        self.pos = pos
        self.name = 'Gun'
        self.front = front
        self.up = [0,1,0]
        self.postMotion = 0.88
        self.frontMotion = 0.02
        self.pitch = 0.0
        self.yaw = -90.0
        self.bulletMat, self.bulletShader = bulletParams
        self.initialPos = pos

    def fire(self):
        new_bullet = Bullet(self.pos,self.front, self.bulletMat, self.bulletShader)
        self.bullets.append(new_bullet)

    def getModelMatrix(self):
        self.move();
        return super().getModelMatrix()
    
    def move(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        x = mouse_dx * self.mouse_sensitivity
        y = -mouse_dy * self.mouse_sensitivity
        self.rotate(y,x, offset =np.array([0,0,0.1]))
        self.pos[0] += x*self.posMotion
        self.pos[1] -= y*self.posMotion
        bullet_offsetx = 0.03
        bullet_offsety = 0.1
        self.pos = [self.initialPos[0]+(self.pos[0]*bullet_offsetx),
        self.initialPos[1]+(self.pos[1]*bullet_offsety),self.pos[2]]
        self.front = np.dot(self.front,self.getRotationMatrix(-y* self.frontMotion, x*self.frontMotion*0.5, 0))



class Target(Shape):
    def __init__(self, vertices, material, shader, FormatAlign=["in_position"], format=['3 0'], stride=3, **kargs):
        super().__init__(vertices, material, shader, FormatAlign, format, stride, **kargs)




class Bullet(Shape):
    def __init__(self, position, direction, material, shader):
        scale = 0.02
        self.vertices = ScaleObjectVertices(getCombinedVertices(getBulletVertices(), getBulletIndices(),[0.9,0.8,0.4]*18), scale,scale,scale)
        self.vertices = shiftObjectVertices(self.vertices, *position)
        super().__init__(self.vertices,  material, shader, ['in_position','in_color'],['3 0','3 3'], 6, xpos = 0)
        self.direction = np.array(direction, dtype = np.float32)
        self.speed = 0.1
        self.name = 'bullet'

    
    def move(self):
        if not (self.vertices[0][2]<-3.6):
            self.translateVert(*self.direction * self.speed)
        

    
    





        