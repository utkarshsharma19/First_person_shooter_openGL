import numpy as np
class Material:
    def __init__(self, ambient =0.2, diffuse_intensity = 0.6, specular_shade = 2.0, Type= None, Texture = None):
        self.texture = Texture
        self.__amb = ambient
        self.__diff = diffuse_intensity
        self.__spec = specular_shade
        self.Type = Type
        self.ambient = [0,0,0]
        self.diffuse_intentsity = [0,0,0]
        self.specular_shade = [0,0,0]
    
    def LightenUp(self, color):
        match self.Type:
            case 'dull':
                self.dull(color)
            case 'bright':
                self.bright(color)
            case 'metallic':
                self.metallic(color)
            case 'dark':
                self.dark(color)
            case 'oily':
                self.oily(color)
            case 'iluminous':
                self.ilumunous(color)
            case _:
                self.ambient = self.__amb * color
                self.diffuse_intentsity = self.__diff * color
                self.specular_shade = self.__spec * color
                
        