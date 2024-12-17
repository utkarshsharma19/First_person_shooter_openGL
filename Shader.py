from OpenGL.GL import *
from OpenGL.GL.shaders import *
class Shader:
    def __init__(self, vertexShader, fragmentShader) :
        with open(vertexShader,'r') as vs:
            vertex_shader_code = vs.read()
        with open(fragmentShader, 'r') as fs:
            fragment_shader_code = fs.read()
        
        self.__vertexShader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
        self.__fragmentShader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)
        self.shaderProgram = compileShader(self.__vertexShader, self.__fragmentShader)

        self.VP_loc = glGetUniformLocation(self.shaderProgram,"VP")
        self.M_loc = glGetUniformLocation(self.shaderProgram,"M")
        self.ambient_loc = glGetUniformLocation(self.shaderProgram,"ambient")
        self.lightPos_loc = glGetUniformLocation(self.shaderProgram,"lightPos")
        self.lightInt_loc = glGetUniformLocation(self.shaderProgram,"lightInt")
        self.diffuseInt_loc = glGetUniformLocation(self.shaderProgram,"diffuseInt")
        self.camPos_loc = glGetUniformLocation(self.shaderProgram,"camPos")
        self.specInt_loc = glGetUniformLocation(self.shaderProgram,"specInt")
        self.texture_sampler_location = glGetUniformLocation(self.shaderProgram,"tex_sampler")

    
    def destroy(self):
        glDetachShader(self.shaderProgram, self.__vertexShader)
        glDeleteShader(self.__vertexShader)
        
        # Detach and delete the fragment shader
        glDetachShader(self.shaderProgram, self.__fragmentShader)
        glDeleteShader(self.__fragmentShader)
        
        # Delete the shader program
        glDeleteProgram(self.shaderProgram)
        
        # Clean up references
        self.shaderProgram = None
        self.__vertexShader = None
        self.__fragmentShader = None




       


