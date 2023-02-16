import Cube
import math3d
import pysdl2.sdl2 as sdl2
class Jellblock:
    cube=None

    def __init__(self,matrix,texture):
        self.worldMatrix=matrix
        if Jellblock.cube==None:
            Jellblock.cube=Cube.Cube(texture)
    def draw(self,prog):
        prog.setUniform("worldMatrix",self.worldMatrix)
        Jellblock.cube.draw(prog)
