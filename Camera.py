from math3d import *

class Camera:
    def __init__(self,**kw):
        self.fov_h = kw.get("fov",45)
        self.hither = kw.get("hither",0.1)
        self.yon = kw.get("yon",1000)
        self.aspect_ratio = kw.get("aspect_ratio",1)
        self.fov_v = 1.0/self.aspect_ratio * self.fov_h
        self.U=vec4([1,0,0,0])
        self.V=vec4([0,1,0,0])
        self.W=vec4([0,0,1,0])
        self.viewmatrix=mat4.identity()
        self.posmatrix=mat4.identity()
        self.eye=vec4([0,0,0,1])
        self.teye=mat4.identity()
        self.compute_proj_matrix()
        self.compute_view_matrix()
         
    def compute_proj_matrix(self):
        self.projmatrix = mat4( 
            1/math.tan(math.radians(self.fov_h)),0,0,0,
            0,1/math.tan(math.radians(self.fov_v)),0,0,
            0,0,1+2*self.yon/(self.hither-self.yon),-1,
            0,0,2*self.hither*self.yon/(self.hither-self.yon),0)
             
    def compute_view_matrix(self):
        self.viewmatrix=mat4.identity()
        
        
        
        UVW=mat4([self.U[0],self.V[0],self.W[0],0,
                 self.U[1],self.V[1],self.W[1],0,
                 self.U[2],self.V[2],self.W[2],0,
                 0,0,0,1])
        
        self.teye=translation([-self.eye[0],-self.eye[1],-self.eye[2]])
                   

        self.viewmatrix=self.teye*UVW
        
        
        
        #print(self.viewmatrix)
        #print(self.eye)
        #print(self.viewmatrix)
    def draw(self,prog):
        prog.setUniform("projMatrix",self.projmatrix)
        
        prog.setUniform("viewMatrix",self.viewmatrix)
        
    def walk(self,amt):
        #walk forward/backward
        M=translation([-amt*self.W[0],-amt*self.W[1],-amt*self.W[2]])
        
        self.eye=self.eye*M
        
        
        
        
        
        self.compute_view_matrix()
    def turn(self,amt):
        M=axisRotation(self.V,amt)

        self.U*=M
        self.W*=M


        

        
        
        
        self.compute_view_matrix()
    def strafe(self,amt):
        M=translation(-amt*self.U)
        self.eye*=M
        self.compute_view_matrix()
    def jump(self,amt):
        M=translation(amt*self.V)
        self.eye=self.eye*M
        self.compute_view_matrix()
    def fall(self,amt):
        M=translation(-amt*self.V)
        self.eye=self.eye*M
        self.compute_view_matrix()
