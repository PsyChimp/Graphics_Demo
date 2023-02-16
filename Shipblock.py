import Cube
import math3d
import pysdl2.sdl2 as sdl2
class Shipblock:
    cube=None

    def __init__(self,matrix,texture):
        self.worldMatrix=matrix
        if Shipblock.cube==None:
            Shipblock.cube=Cube.Cube(texture)
    def draw(self,prog):
        prog.setUniform("worldMatrix",self.worldMatrix)
        Shipblock.cube.draw(prog)
