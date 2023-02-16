import Mesh
import math3d
import pysdl2.sdl2 as sdl2
from math3d import *
class Raygun:
    mesh=None

    def __init__(self,fname,matrix,texture):
        self.worldMatrix=matrix
        self.U=vec4([1,0,0,0])
        self.V=vec4([0,1,0,0])
        self.W=vec4([0,0,1,0])
        self.pos=vec4([matrix[3][0],matrix[3][1]+0.3,matrix[3][2],1])
        if Raygun.mesh==None:
            Raygun.mesh=Mesh.Mesh(fname,texture)
    def compute_world_matrix(self):
        self.worldMmatrix=mat4.identity()
        
        
        
        UVW=mat4([self.U[0],self.V[0],self.W[0],0,
                 self.U[1],self.V[1],self.W[1],0,
                 self.U[2],self.V[2],self.W[2],0,
                 0,0,0,1])
        
        self.teye=translation([-self.pos[0],-self.pos[1],-self.pos[2]])
                   

        self.worldMatrix=self.teye*UVW
    def turn(self,amt):
        M=axisRotation(self.V,amt)

        self.U*=M
        self.W*=M


        self.compute_world_matrix()
    def draw(self,prog):
        prog.setUniform("worldMatrix",self.worldMatrix)
        self.pos=vec4([self.worldMatrix[3][0],self.worldMatrix[3][1]+0.3,self.worldMatrix[3][2],0])
        Raygun.mesh.draw(prog)
