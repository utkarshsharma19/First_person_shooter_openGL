import pygame as pg 
from GameEngine import GameEngine
from OpenGL.GL import *
import glm



class Renderer:
    def __init__(self,shapes, camera,light,fbo=None,miniCamScreen=None, staticCamera=None) -> None:
        self.shapes = shapes
        self.camera = camera
        self.light = light
        self.fbo = fbo
        self.miniCamScreen = miniCamScreen
        self.staticCamera = staticCamera
        [shape.material.LightenUp(self.light.color) for shape in self.shapes]

    
    def draw(self, shape,static=False):
        glUseProgram(shape.shader.shader_program)
        glBindVertexArray(shape.vao)
        self.Update_MVP(shape, static)
        if not shape.name =='Bullet':
            self.loadLights(shape)
            if shape.material.texture:
                self.loadTexture(shape)
    


        self.loadLight(shape)
        if shape.material.texture:
            self.LoadTexture(shape)
        glDrawArrays(GL_TRIANGLES, 0, len(shape.vertices))
        glBindVertexArray(0)

    def render(self, shapes):
        glClearColor(*self.camera.bgColor, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for shape in shapes:
            self.draw(shape)
            if(shape.name=='Gun'):
                for b in shape.bullets:
                    self.draw(b)
        if self.fbo:
            glBindFramebuffer(GL_FRAMEBUFFER, self.fbo.fbo)
            glClearColor(*self.staticCamera.bgColor,1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            for shapes in self.shapes:
                self.draw(shapes, True)
            glBindFramebuffer(GL_FRAMEBUFFER,0)
            glUseProgram(self.miniCamScreen.shader.shader_program)
            glBindVertexArray(self.miniCam.vao)
            glBindTexture(GL_TEXTURE_2D, self.miniCamScreen.material.texture.texture_id)
            self.Update_MVP(self.miniCamScreen, True)
            glDrawArrays(GL_TRIANGLES, 0, len(self.miniCamScreen.vertices))
            glBindVertexArray(0)
    
    def Update_MVP(self,shape,static=False):
        model = shape.getModelMatrix()
        if static:
            view = self.staticCamera.get_view()
            projection = self.staticCamera.get_projection()
        else:
            view = self.camera.get_view()
            projection = self.camera.get_projection()
        VP = projection * view
        glUniformMatrix4fv(shape.shader.VP_loc, 1,GL_FALSE,glm.value_ptr(VP))
        glUniformMatrix4fv(shape.shader.M_loc, 1,GL_FALSE,model)
    
    def loadLights(self,shape):
        glUniform3fv(shape.shader.ambient_loc,1,shape.material.ambient)
        glUniform3fv(shape.shader.diffuseInt_loc,1,shape.material.diffuse_intensity)
        glUniform3fv(shape.shader.specInt_loc,1,shape.material.specular_sahde)
        glUniform3fv(shape.shader.lightPos_loc,1,self.light.pos)
        glUniform3fv(shape.shader.lightInt_loc,1,self.light.intensity)
        glUniform3fv(shape.shader.camPos_loc,1,self.camera.pos)
    
    def loadTexture(self, shape):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, shape.material.texture.texture_id)
        glUniform1i(shape.shader.texture_sampler_location, 0)


        

    def destory(self):
        for shape in self.shapes:
            shape.destroy()
        if self.fbo:
            self.fbo.destroy()
            self.miniCamScreen.destroy()


