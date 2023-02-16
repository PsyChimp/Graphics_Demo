import Plane
import math3d
import pysdl2.sdl2 as sdl2
import Program
from glfuncs import *
from glconstants import *
class Floor:
    plane=None

    def __init__(self,matrix,texture):
        self.worldMatrix=matrix
        if Floor.plane==None:
            Floor.plane=Plane.Plane(texture)
            
    def draw(self,prog):
        prog.setUniform("worldMatrix",self.worldMatrix)
        Floor.plane.draw(prog)
