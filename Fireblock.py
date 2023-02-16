import Cube
import math3d
import pysdl2.sdl2 as sdl2
class Fireblock:
    cube=None

    def __init__(self,matrix,texture):
        self.worldMatrix=matrix
        if Fireblock.cube==None:
            Fireblock.cube=Cube.Cube(texture)
    def draw(self,prog):
        prog.setUniform("worldMatrix",self.worldMatrix)
        Fireblock.cube.draw(prog)
