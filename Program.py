from glfuncs import *
from glconstants import *
from Texture import *
import array
import math3d

class Program:
    POSITION_INDEX = 0
    COLOR_INDEX = 1
    TEXCOORD_INDEX = 2
    NORMAL_INDEX = 3
    OFFSET_INDEX = 4
    BONE_INDEX = 5
    
    class FloatSetter:
        def __init__(self,name,loc):
            self.name=name 
            self.loc = loc
        def set(self,value):
            v = float(value)
            glUniform1f( self.loc, v )

    class Sampler2dSetter:
        def __init__(self,name,loc,unit):
            self.name=name 
            self.loc = loc
            self.unit = unit
        def set(self,value):
            if not isinstance(value,Texture2D):
                raise RuntimeError("Not the correct type")
            value.bind(self.unit)
            glUniform1i( self.loc, self.unit )
            
    class Sampler2dArraySetter:
        def __init__(self,name,loc,unit):
            self.name=name 
            self.loc = loc
            self.unit = unit
        def set(self,value):
            if not isinstance(value,ImageTextureArray):
                raise RuntimeError("Not the correct type")
            value.bind(self.unit)
            glUniform1i( self.loc, self.unit )

    class Vec2Setter:
        def __init__(self,name,loc):
            self.name=name 
            self.loc = loc
        def set(self,v):
            if type(v) != math3d.vec2:
                raise RuntimeError("Not the correct type")
            glUniform2f( self.loc, v.x, v.y )

    class Vec3Setter:
        def __init__(self,name,loc):
            self.name=name 
            self.loc = loc
        def set(self,v):
            if type(v) != math3d.vec3:
                raise RuntimeError("Not the correct type")
            glUniform3f( self.loc, v.x, v.y, v.z )
            
    class Vec4ArraySetter:
        def __init__(self,name,loc,size):
            self.name=name 
            self.loc = loc
            self.size = size
        def set(self,v):
            if type(v) == array.array:
                if len(v) != 4*self.size:
                    raise RuntimeError("Wrong length: Expected "+str(self.size*4)+" floats but got "+str(len(v)))
                else:
                    tmp = v
                    lt = len(tmp)//4
            else:
                if len(v) != self.size:
                    raise RuntimeError("Wrong length: Expected "+str(self.size)+" vec4's but got "+str(len(v)))
                tmp=[]
                for q in v:
                    tmp += [q.x,q.y,q.z,q.w]
                tmp = array.array('f',tmp)
                lt = len(tmp)
                
            glUniform4fv( self.loc, lt, tmp )

    class Vec3ArraySetter:
        def __init__(self,name,loc,size):
            self.name=name 
            self.loc = loc
            self.size = size
        def set(self,v):
            if type(v) == array.array:
                if len(v) != 3*self.size:
                    raise RuntimeError("Wrong length: Expected "+str(self.size*3)+" floats but got "+str(len(v)))
                else:
                    tmp = v
                    lt = len(tmp)//4
            else:
                if len(v) != self.size:
                    raise RuntimeError("Wrong length: Expected "+str(self.size)+" vec3's but got "+str(len(v)))
                tmp=[]
                for q in v:
                    tmp += [q.x,q.y,q.z]
                tmp = array.array('f',tmp)
                lt = len(tmp)
                
            glUniform3fv( self.loc, lt, tmp )



    class Mat4Setter:
        def __init__(self,name,loc):
            self.name=name 
            self.loc = loc
        def set(self,v):
            if type(v) != math3d.mat4:
                raise RuntimeError("Not the correct type")
            glUniformMatrix4fv( self.loc, 1,True,v.tobytes() )

    def __init__(self,vsfname,fsfname):
        self.warned=set()
        
        tmp = array.array("I",[0])
        
        vs = self.make_shader(vsfname, GL_VERTEX_SHADER)
        fs = self.make_shader(fsfname, GL_FRAGMENT_SHADER)
        prog = glCreateProgram()
        glAttachShader(prog,vs)
        glAttachShader(prog,fs)
        
        glBindAttribLocation(prog,Program.POSITION_INDEX, "a_position")
        glBindAttribLocation(prog,Program.COLOR_INDEX, "a_color")
        glBindAttribLocation(prog,Program.TEXCOORD_INDEX, "a_texcoord")
        glBindAttribLocation(prog,Program.NORMAL_INDEX, "a_normal")
        glBindAttribLocation(prog,Program.OFFSET_INDEX, "a_offset")
        glBindAttribLocation(prog,Program.BONE_INDEX, "a_boneidx")
        
        glLinkProgram(prog)
        infolog = bytearray(4096)
        glGetProgramInfoLog(prog,len(infolog),tmp,infolog)
        if tmp[0] > 0:
            infolog = infolog[:tmp[0]].decode()
            print("Linking",vsfname,"+",fsfname,":")
            print(infolog)
        glGetProgramiv( prog, GL_LINK_STATUS, tmp )
        if not tmp[0]:
            raise RuntimeError("Could not link shaders")
        self.prog = prog
        
        self.uniforms={}
        texcounter=0
        glGetProgramiv(prog,GL_ACTIVE_UNIFORMS, tmp)
        numuniforms = tmp[0]
        for i in range(numuniforms):
            type_ = array.array("I",[0])
            size = array.array("I",[0])
            index = array.array("I",[0])
            name = array.array("B",[0]*256)
            le = array.array("I",[0])
            
            tmp[0] = i
            
            glGetActiveUniformsiv(prog,1,tmp,GL_UNIFORM_TYPE,type_)
            glGetActiveUniformsiv(prog,1,tmp,GL_UNIFORM_SIZE,size)
            glGetActiveUniformName(prog,i,len(name),le, name)
            name = name[:le[0]].tobytes().decode()
            loc = glGetUniformLocation(prog,name )
            
            if type_[0] == GL_FLOAT and size[0] == 1:
                setter = Program.FloatSetter(name,loc)
            elif type_[0] == GL_FLOAT_VEC2 and size[0] == 1:
                setter = Program.Vec2Setter(name,loc)
            elif type_[0] == GL_FLOAT_VEC3 and size[0] == 1:
                setter = Program.Vec3Setter(name,loc)
            elif type_[0] == GL_FLOAT_VEC4 and size[0] > 1:
                setter = Program.Vec4ArraySetter(name,loc,size[0])
            elif type_[0] == GL_FLOAT_VEC3 and size[0] > 1:
                setter = Program.Vec3ArraySetter(name,loc,size[0])
            elif type_[0] == GL_FLOAT_MAT4 and size[0] == 1:
                setter = Program.Mat4Setter(name,loc)
            elif type_[0] == GL_SAMPLER_2D and size[0] == 1:
                setter = Program.Sampler2dSetter(name,loc,texcounter)
                texcounter += 1
            elif type_[0] == GL_SAMPLER_2D_ARRAY and size[0] == 1:
                setter = Program.Sampler2dArraySetter(name,loc,texcounter)
                texcounter += 1
            else:
                raise RuntimeError("Don't know about type of "+name)
            
            self.uniforms[name] = setter

    def setUniform(self,name,value):
        if Program.active != self:
            raise RuntimeError("Cannot set uniform on non-active program")
        if name in self.uniforms:
            self.uniforms[name].set(value)
        elif name not in self.warned:
            self.warned.add(name)
            print("No such uniform",name)
            

            
    def use(self):
        glUseProgram(self.prog)
        Program.active = self
        
    def make_shader(self, filename, shadertype ):
        shaderdata = open(filename).read()
        s = glCreateShader( shadertype )
        glShaderSource( s,1,[shaderdata],None)
        glCompileShader( s )
        infolog = bytearray(4096)
        tmp = array.array("I",[0])
        glGetShaderInfoLog( s, len(infolog), tmp, infolog)
        if tmp[0] > 0 :
            infolog = infolog[:tmp[0]].decode()
            print("When compiling",shadertype,filename,":")
            print(infolog)
        glGetShaderiv( s, GL_COMPILE_STATUS, tmp )
        if not tmp[0]:
            raise RuntimeError("Cannot compile "+filename)
        return s
