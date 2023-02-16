from glfuncs import *
from glconstants import *
from Program import *
from Texture import *
import pysdl2.sdl2 as sdl2
import sys
from ctypes import *

class Mesh:
    def __init__(self,fname,texture):
        fp=open(fname,'rb')
        if 1:
            line=fp.readline().decode().strip()
            assert line=="mesh_01"
            while 1:
                
                line=fp.readline().decode().strip()
                
                if line=="end":
                    break
                elif line.startswith("num_vertices"):
                    lst=line.split()
                    self.numv=int(lst[1])
                elif line.startswith("num_triangles"):
                    lst=line.split()
                    self.numt=int(lst[1])
                elif line.startswith("texture_file"):
                    lst=line.split()
                    
                elif line.startswith("vertices"):
                    numbytes=self.numv*3*4
                    vdata=fp.read(numbytes)
                elif line.startswith("texcoords"):
                    numbytes=self.numv*2*4
                    tdata=fp.read(numbytes)
                elif line.startswith("normals"):
                    numbytes=self.numv*3*4
                    ndata=fp.read(numbytes)
                elif line.startswith("indices"):
                    numbytes=self.numt*3*2
                    idata=fp.read(numbytes)
                    
                else:
                    pass
                
        tmp=array.array("I",[0])
        glGenVertexArrays(1,tmp)
        self.vao = tmp[0]
        glBindVertexArray(self.vao)
        self.tex=texture
        glGenBuffers(1,tmp)
        self.vbuff = tmp[0]
        glBindBuffer(GL_ARRAY_BUFFER,self.vbuff)
        glBufferData(GL_ARRAY_BUFFER,len(vdata),vdata,GL_STATIC_DRAW)
        glEnableVertexAttribArray(Program.POSITION_INDEX)
        glVertexAttribPointer(Program.POSITION_INDEX,3,GL_FLOAT,False,3*4,0)

        assert len(ndata) == len(vdata)
        
        glGenBuffers(1,tmp)
        self.nbuff = tmp[0]
        glBindBuffer(GL_ARRAY_BUFFER,self.nbuff)
        glBufferData(GL_ARRAY_BUFFER,len(ndata),ndata,GL_STATIC_DRAW)
        glEnableVertexAttribArray(Program.NORMAL_INDEX)
        glVertexAttribPointer(Program.NORMAL_INDEX,3,GL_FLOAT,False,3*4,0)

        glGenBuffers(1,tmp)
        self.tbuff = tmp[0]
        glBindBuffer(GL_ARRAY_BUFFER,self.tbuff)
        glBufferData(GL_ARRAY_BUFFER,len(tdata),tdata,GL_STATIC_DRAW)
        glEnableVertexAttribArray(Program.TEXCOORD_INDEX)
        glVertexAttribPointer(Program.TEXCOORD_INDEX,2,GL_FLOAT,False,2*4,0)

        glGenBuffers(1,tmp)
        self.ibuff = tmp[0]
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.ibuff)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(idata),idata,GL_STATIC_DRAW)
 
        glBindVertexArray(0)
    def draw(self,prog):
        prog.setUniform("tex",self.tex)
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.numt*3, GL_UNSIGNED_SHORT, 0 )

