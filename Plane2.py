from glfuncs import *
from glconstants import *
from Program import *
from Texture import *

class Plane2:
    def __init__(self,texture):
        tmp=array.array("I",[0])
        glGenVertexArrays(1,tmp)
        self.vao = tmp[0]
        
        glBindVertexArray(self.vao)
        self.tex=texture
        glGenBuffers(1,tmp)
        self.vbuff = tmp[0]
        glBindBuffer(GL_ARRAY_BUFFER,self.vbuff)
        vdata = array.array('f',
            [#top
             -0.5,0,-0.5,
             -0.5,0,0.5,
             0.5,0,-0.5,
             0.5,0,0.5,
             #bot
             -0.5,0,-0.5,
             -0.5,0,0.5,
             0.5,0,-0.5,
             0.5,0,0.5
             ])
        
        glBufferData(GL_ARRAY_BUFFER,len(vdata)*4,vdata,GL_STATIC_DRAW)
        glEnableVertexAttribArray(Program.POSITION_INDEX)
        glVertexAttribPointer(Program.POSITION_INDEX,3,GL_FLOAT,False,3*4,0)
        #normal data
        ndata = array.array("f",[
            #top face
            0,-1,0,
            0,-1,0,
            0,-1,0,
            0,-1,0,
            #bot face
            0,-1,0,
            0,-1,0,
            0,-1,0,
            0,-1,0
            
        ])
        assert len(ndata) == len(vdata)
        
        glGenBuffers(1,tmp)
        self.nbuff = tmp[0]
        glBindBuffer(GL_ARRAY_BUFFER,self.nbuff)
        glBufferData(GL_ARRAY_BUFFER,len(ndata)*4,ndata,GL_STATIC_DRAW)
        glEnableVertexAttribArray(Program.NORMAL_INDEX)
        glVertexAttribPointer(Program.NORMAL_INDEX,3,GL_FLOAT,False,3*4,0)
        #texture data
        tdata = array.array("f",[
            #top
            0,0,
            1,0,
            0,1,
            1,1,
            #bot
            0,0,
            1,0,
            0,1,
            1,1
            ])
        glGenBuffers(1,tmp)
        self.tbuff = tmp[0]
        glBindBuffer(GL_ARRAY_BUFFER,self.tbuff)
        glBufferData(GL_ARRAY_BUFFER,len(tdata)*4,tdata,GL_STATIC_DRAW)
        glEnableVertexAttribArray(Program.TEXCOORD_INDEX)
        glVertexAttribPointer(Program.TEXCOORD_INDEX,2,GL_FLOAT,False,2*4,0)
        idata = array.array("H",[
            0,1,2,
            1,2,3,
            0,1,2,
            1,2,3
            ])
        glGenBuffers(1,tmp)
        self.ibuff = tmp[0]
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.ibuff)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(idata)*2,idata,GL_STATIC_DRAW)
 
        glBindVertexArray(0)
    def draw(self,prog):
        prog.setUniform("tex",self.tex)
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_SHORT, 0 )
