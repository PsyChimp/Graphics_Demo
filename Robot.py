import Mesh
import math3d
import pysdl2.sdl2 as sdl2
from math3d import *
class Robot:
    mesh=None

    def __init__(self,fname,matrix,texture):
        self.worldMatrix=matrix
        self.pos=vec4([matrix[3][0],matrix[3][1]+0.3,matrix[3][2],0])
        self.alpha=1
        self.timer=None
        if Robot.mesh==None:
            Robot.mesh=Mesh.Mesh(fname,texture)
    def draw(self,prog):
        prog.setUniform("worldMatrix",self.worldMatrix)
        Robot.mesh.draw(prog)
