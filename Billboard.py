from glfuncs import *
from glconstants import *
from Program import *
from Texture import *
class Board:
    def __init__(self,positions,texture):
        
        tmp=array.array("I",[0])
        glGenVertexArrays(1,tmp)
        self.vao = tmp[0]
        
        glBindVertexArray(self.vao)
        self.tex=texture
        glGenBuffers(1,tmp)
        self.vbuff = tmp[0]
        glBindBuffer(GL_ARRAY_BUFFER,self.vbuff)
        vdata = array.array('f',
            [#front
             0.5,0.5,0,
             -0.5,0.5,0,
             0.5,-0.5,0,
             -0.5,-0.5,0,
             -0.5,0.5,0,
             0.5,-0.5,0
             ])
        
        glBufferData(GL_ARRAY_BUFFER,len(vdata)*4,vdata,GL_STATIC_DRAW)
        glEnableVertexAttribArray(Program.POSITION_INDEX)
        glVertexAttribPointer(Program.POSITION_INDEX,3,GL_FLOAT,False,3*4,0)
        #texture data
        tdata = array.array("f",[
            #front
            0,1,
            1,1,
            0,0,
            1,0,
            1,1,
            0,0
            ])
        glGenBuffers(1,tmp)
        self.tbuff = tmp[0]
        glBindBuffer(GL_ARRAY_BUFFER,self.tbuff)
        glBufferData(GL_ARRAY_BUFFER,len(tdata)*4,tdata,GL_STATIC_DRAW)
        glEnableVertexAttribArray(Program.TEXCOORD_INDEX)
        glVertexAttribPointer(Program.TEXCOORD_INDEX,2,GL_FLOAT,False,2*4,0)
        idata = array.array("H",[
            0,1,2,
            1,2,3
            ])
        glGenBuffers(1,tmp)
        self.ibuff = tmp[0]
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.ibuff)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(idata)*2,idata,GL_STATIC_DRAW)
 
        glBindVertexArray(0)
    def draw(self,prog,bullets):
        prog.setUniform("tex",self.tex)
        numinstances=len(bullets)
        if numinstances!=0:
            locationArray=[]
            for bullet in bullets:
                locationArray.append(bullet.x)
                locationArray.append(bullet.y)
                locationArray.append(bullet.z)
            locationArray=array.array('f',locationArray)
            glBindVertexArray(self.vao)
            tmp = array.array("I",[0])
            glGenBuffers(1,tmp)
            locbuff = tmp[0]
            glBindBuffer(GL_ARRAY_BUFFER,locbuff)
            glBufferData(GL_ARRAY_BUFFER,len(locationArray)*4, locationArray, GL_DYNAMIC_DRAW )
            glEnableVertexAttribArray(Program.OFFSET_INDEX)
            glVertexAttribPointer(Program.OFFSET_INDEX,3,GL_FLOAT,False,3*4,0)
            #make it instanced
            glVertexAttribDivisor(Program.OFFSET_INDEX , 1)
            glBindVertexArray(0)

            glBindVertexArray(self.vao)
            glDrawArraysInstanced(GL_TRIANGLES,0,36,numinstances)
