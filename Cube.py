from glfuncs import *
from glconstants import *
from Program import *
from Texture import *

class Cube:
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
            [

                #top face
                -0.5,0.5,0.5,  #0
                0.5,0.5,0.5,   #1
                -0.5,0.5,-0.5, #2
                -0.5,0.5,-0.5, #2
                0.5,0.5,-0.5,  #3
                0.5,0.5,0.5,   #1
                #right face
                0.5,0.5,0.5,   #4
                0.5,0.5,-0.5,  #5
                0.5,-0.5,0.5,  #6
                0.5,-0.5,0.5,
                0.5,-0.5,-0.5, #7
                0.5,0.5,-0.5,
                #back face
                0.5,-0.5,-0.5, #8
                -0.5,-0.5,-0.5,#9
                
                0.5,0.5,-0.5,  #10
                0.5,0.5,-0.5,
                -0.5,-0.5,-0.5,
                -0.5,0.5,-0.5, #11
                #left face
                -0.5,0.5,-0.5, #12
                -0.5,0.5,0.5,  #13
                
                -0.5,-0.5,-0.5,#14
                -0.5,-0.5,-0.5,
                -0.5,0.5,0.5,
                -0.5,-0.5,0.5, #15
                #bot face
                -0.5,-0.5,0.5, #16
                0.5,-0.5,0.5,  #17
                0.5,-0.5,-0.5, #18
                -0.5,-0.5,0.5,
                0.5,-0.5,-0.5,
                -0.5,-0.5,-0.5,#19
                #front face
                -0.5,-0.5,0.5, #20
                0.5,-0.5,0.5,  #21
                
                -0.5,0.5,0.5,  #22
                -0.5,0.5,0.5,
                0.5,-0.5,0.5,
                0.5,0.5,0.5    #23

                
            ]
        )
        glBufferData(GL_ARRAY_BUFFER,len(vdata)*4,vdata,GL_STATIC_DRAW)
        glEnableVertexAttribArray(Program.POSITION_INDEX)
        glVertexAttribPointer(Program.POSITION_INDEX,3,GL_FLOAT,False,3*4,0)

        #normal data
        ndata = array.array("f",[
            #top face
            0,1,0,
            0,1,0,
            0,1,0,
            0,1,0,
            0,1,0,
            0,1,0,
            #right face
            1,0,0,
            1,0,0,
            1,0,0,
            1,0,0,
            1,0,0,
            1,0,0,
            #back face
            0,0,-1,
            0,0,-1,
            0,0,-1,
            0,0,-1,
            0,0,-1,
            0,0,-1,
            #left face
            -1,0,0,
            -1,0,0,
            -1,0,0,
            -1,0,0,
            -1,0,0,
            -1,0,0,
            #bot face
            0,-1,0,
            0,-1,0,
            0,-1,0,
            0,-1,0,
            0,-1,0,
            0,-1,0,
            #front face
            0,0,1,
            0,0,1,
            0,0,1,
            0,0,1,
            0,0,1,
            0,0,1
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
                #top face
                0,0,  #0
                1,0,   #1
                0,1,  #2
                0,1,  #2
                1,1,   #3
                0,1,   #1
                #right face
                0,0,  #0
                1,0,   #1
                0,1,  #2
                0,1,  #2
                1,1,   #3
                1,0,   #1
                #back face
                0,0,  #0
                1,0,   #1
                0,1,  #2
                0,1,  #2
                1,0,   #3
                1,1,   #1
                #left face
                0,0,  #0
                1,0,   #1
                0,1,  #2
                0,1,  #2
                1,0,   #3
                1,1,   #1
                #bot face
                0,0,  #0
                1,0,   #1
                0,1,  #2
                0,1,  #2
                1,0,   #3
                1,1,   #1
                #front face
                0,0,  #0
                1,0,   #1
                0,1,  #2
                0,1,  #2
                1,0,   #3
                1,1,   #1
        ])
        
        glGenBuffers(1,tmp)
        self.tbuff = tmp[0]
        glBindBuffer(GL_ARRAY_BUFFER,self.tbuff)
        glBufferData(GL_ARRAY_BUFFER,len(tdata)*4,tdata,GL_STATIC_DRAW)
        glEnableVertexAttribArray(Program.TEXCOORD_INDEX)
        glVertexAttribPointer(Program.TEXCOORD_INDEX,2,GL_FLOAT,False,2*4,0)

        
    def draw(self,prog,bricks,textures):
        
        prog.setUniform("tex2",textures)
        numinstances=len(bricks)
        if numinstances!=0:
            locationArray=[]
            for brick in bricks:
                locationArray.append(brick.x)
                locationArray.append(brick.y)
                locationArray.append(brick.z)
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
        
            
