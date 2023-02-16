import Plane2
import math3d
import pysdl2.sdl2 as sdl2
class Roof:
    plane=None

    def __init__(self,matrix,texture):
        self.worldMatrix=matrix
        if Roof.plane==None:
            Roof.plane=Plane2.Plane2(texture)
    def draw(self,prog):
        prog.setUniform("worldMatrix",self.worldMatrix)
        Roof.plane.draw(prog)
