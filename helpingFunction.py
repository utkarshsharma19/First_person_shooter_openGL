


from math import radians
import pywavefront as pwd
import numpy as np

def getCombinedVertices(vertices, indices, normals, tex_coords, Index=False):
    combined_vertices = []
    for i in indices:
        # Combine position, normal, and texture data
        vertex = [
            *vertices[i],
            *normals[3 * i: 3 * i + 3],
            *tex_coords[2 * i: 2 * i + 2],
        ]
        combined_vertices.append(vertex)

    combined_vertices = np.array(combined_vertices, dtype=np.float32)

    if Index:
        return combined_vertices
    else:
        return combined_vertices.flatten()

def shiftObjectVertices(vertices, x=0,y=0,z=0, xpos = 0,ypos = 1,zpos = 2):
    return np.array(list(map(lambda a: [ *a[:xpos], a[xpos]+x, a[ypos]+y, a[zpos]+z, *a[zpos+1:]], vertices)))


def ScaleObjectVertices(vertices, x=1,y=1,z=1, xpos = 0,ypos = 1,zpos = 2):
    return np.array(list(map(lambda a: [ *a[:xpos], float(a[xpos])*x, float(a[ypos])*y, float(a[zpos])*z, *a[zpos+1:]], vertices)))

def rotateObjectVertices(vertices, x =0 ,y=0, z=0, xpos =0, ypos =1, zpos = 2, translated=[0,0,0]):
    vertices = shiftObjectVertices(vertices, *translated, xpos,ypos,zpos)
    x,y,z = radians(x), radians(y), radians(z)

    Rx = np.array([[1,0,0],
                    [0,np.cos(x), -np.sin(x)],
                    [0,np.sin(x),np.sin(y)]])

    Ry = np.array([[np.cos(y),1,np.sin(y)],
                    [0,1, 0],
                    [-np.sin(y),0,np.cos(y)]])


    Rz= np.array([[np.cos(z),-np.sin(x),0],
                [np.sin(z),np.cos(z),0],
                [0,0,1]])
    combined = np.array(np.dot(Rx, np.dot(Ry, Rz)))
    vertices = np.array(list(map(lambda a: [*a[:xpos], *np.dot([a[xpos],a[ypos],a[zpos]], combined), *a[zpos+1:]], vertices)))

def getFloorTileVertices():
    return np.array([[0,0,0],[1,0,0],[1,0,1],[0,0,1]])

def getFloorTileIndices():
    return np.array([0,1,2,2,3,0])

def getObjectVertices(OBJname):
    objs = pwd.Wavefront(OBJname, cache=True,parse = True)
    obj = objs.materials.popitem()[1]
    return np.array(obj.vertices, dtype=np.float32)

def getOBJVerticesOriented(name, shift,scale = 0.01, rotation = [0,0,0]):
    V = np.array(getObjectVertices(name))
    V = V.reshape(V.size//8,8)
    scaleObj = scale
    vertObj = ScaleObjectVertices(V, scaleObj, scaleObj,scaleObj,5,6,7)
    vertObj = rotateObjectVertices(vertObj, *rotation, 5,6,7)
    vertObj = shiftObjectVertices(vertObj, *shift, 5,6,7)
    return vertObj
def getBulletVertices():
    # Bullet vertex positions (vertex array) for a simple bullet shape
    vertices = np.array([
        # Positions         # Colors
        0.0,  0.0,  0.0,    1.0, 0.0, 0.0,  # Center
        0.0,  0.02, 0.0,    1.0, 0.0, 0.0,  # Top
        0.01, 0.02, 0.0,    1.0, 0.0, 0.0,  # Top-right
        -0.01, 0.02, 0.0,   1.0, 0.0, 0.0,  # Top-left
        0.01, 0.0, 0.0,     1.0, 0.0, 0.0,  # Bottom-right
        -0.01, 0.0, 0.0,    1.0, 0.0, 0.0,  # Bottom-left
        0.01, -0.02, 0.0,   1.0, 0.0, 0.0,  # Bottom-right (for bottom of the bullet)
        -0.01, -0.02, 0.0,  1.0, 0.0, 0.0,  # Bottom-left (for bottom of the bullet)
    ], dtype=np.float32)

    return vertices

def getBulletIndices():
    
    indices = np.array([
        0, 1, 2,  # Top triangle
        0, 2, 3,  # Top triangle
        0, 3, 4,  # Bottom triangle
        0, 4, 5,  # Bottom triangle
        1, 6, 2,  # Top-right triangle
        2, 6, 3,  # Top-right triangle
        2, 7, 3,  # Top-left triangle
        3, 7, 4,  # Top-left triangle
        4, 7, 5,  # Bottom-right triangle
        5, 7, 6   # Bottom-left triangle
    ], dtype=np.uint32)

    return indices
