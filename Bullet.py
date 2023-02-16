import Billboard
import math
import time
from math3d import *
import pysdl2.sdl2 as sdl2
class Bullet:
    board=None
    def __init__(self,positions,texture):
        #self.worldMatrix=matrix
        #self.pos=cam.eye
        #self.up=vec4([0,1,0,0])
        #self.W=cam.eye-self.pos
        #self.U=cross(self.up,self.W)
        #self.V=cross(self.W,self.U)
        #self.dir=vec4([0,0,1,0])
        #self.mov=-1*cam.W
        #self.angle=0
        self.lifespan=time.time()+5
        self.birth=time.time()
        if Bullet.board==None:
            Bullet.board=Billboard.Board(positions,texture)
    def draw(self,prog,bullets,vel):
        for i in range(len(bullets)):
            
            bullets[i]+=-vel[i]*0.1
        #self.worldMatrix*=translation(self.mov*0.01)
        #self.pos=vec4([self.worldMatrix[3][0],self.worldMatrix[3][1],self.worldMatrix[3][2],1])
        #prog.setUniform("worldMatrix",self.worldMatrix)
        Bullet.board.draw(prog,bullets)
