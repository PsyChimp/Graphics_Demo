import sys
from ctypes import *
import time
import math
import pysdl2.sdl2 as sdl2
from pysdl2.sdl2.keycode import *
from glfuncs import *
from glconstants import *

from Program import *
from math3d import * 
from Texture import *
import time
from Cube import *
from Billboard import *
from Bullet import *
from Camera import *
from Shipblock import *
from Jellblock import *
from Fireblock import *
from Roof import *
from Plane import *
from Plane2 import *
from Floor import *
from Robot import *
from Mesh import *
from Raygun import *
def debugcallback(source,typ, id_,severity, length, message, obj ):
    print(message)

def ranges_overlap(a,b,  c,d):
    return  (c<b and d>a ) or (a<d and b>c)

sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
win = sdl2.SDL_CreateWindow( b"ETGG",20,20, 512,512, sdl2.SDL_WINDOW_OPENGL)
if not win:
    print("Could not create window")
    raise RuntimeError()

sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_STENCIL_SIZE, 8)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION,3)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION,3)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_FLAGS,sdl2.SDL_GL_CONTEXT_DEBUG_FLAG)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
sdl2.SDL_SetRelativeMouseMode(True)

rc = sdl2.SDL_GL_CreateContext(win)
if not rc:
    print("Cannot create GL context")
    raise RuntimeError()
    
glDebugMessageControl(GL_DONT_CARE,GL_DONT_CARE,GL_DONT_CARE, 0, None, 1 )
glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)


glDebugMessageCallback(debugcallback,None)
angle=0
worldMatrix=translation([0,0,0])
gunMatrix=scaling([0.25,0.25,0.25])*axisRotation(vec3([1,0,0]),math.radians(90))*axisRotation(vec3([0,1,0]),math.radians(180))*translation([0.2,0,-0.5])
tex1 = ImageTexture("ship.png")
tex2 = ImageTexture("fire.png")
tex3 = ImageTexture("jellyfish.png")
tex4 = ImageTexture("brick.png")
tex5 = ImageTexture("grass.png")
tex6 = ImageTexture("bullet.png")
tex7 = ImageTexture("robot.png")
tex8 = ImageTexture("guntex.001.png")

#gun=Raygun("raygun.mesh",axisRotation(vec3([1,0,0]),math.radians(90))*axisRotation(vec3([0,1,0]),math.radians(180))*scaling([0.5,0.5,0.5])*translation([0.3,0,-1]),tex8)
textures=[]
#texindex=[]
#textures.append("ship.png")
#textures.append("fire.png")
#textures.append("jellyfish.png")

bricks=[]
tiles=[]
bullets=[]
vel=[]
life=[]
bullet=Bullet(bullets,tex6)
robots=[]
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LEQUAL)

jump_time=time.time()
fall_time=time.time()
jump=False
hit=False
fh=open("world.txt","r")

robots.append(Robot("robot.mesh",scaling([0.75,0.75,0.75])*translation([0,-0.5,-1]),tex7))
robots.append(Robot("robot.mesh",scaling([0.75,0.75,0.75])*translation([3,-0.5,-5]),tex7))
robots.append(Robot("robot.mesh",scaling([0.75,0.75,0.75])*translation([-5,-0.5,-2]),tex7))
gun=Raygun("raygun.mesh",gunMatrix,tex8)
brick=Cube.Cube(tex2)
index_=0
for line in fh:
    line=line.strip()
    print(line)
    index_2=0
    for element in line:
        
        if element==" ":
            tiles.append(Roof(translation([index_2-len(line)/2,0.5,3-index_]),tex4))
            tiles.append(Floor(translation([index_2-len(line)/2,-0.5,3-index_]),tex5))
            index_2+=1
        if element=="*":
            tiles.append(Roof(translation([index_2-len(line)/2,0.5,3-index_]),tex4))
            tiles.append(Floor(translation([index_2-len(line)/2,-0.5,3-index_]),tex5))
            bricks.append(vec3([index_2-len(line)/2,0,3-index_]))
            textures.append("ship.png")
            index_2+=1
        if element=="$":
            tiles.append(Roof(translation([index_2-len(line)/2,0.5,3-index_]),tex4))
            tiles.append(Floor(translation([index_2-len(line)/2,-0.5,3-index_]),tex5))
            bricks.append(vec3([index_2-len(line)/2,0,3-index_]))
            textures.append("fire.png")
            index_2+=1
        if element=="%":
            tiles.append(Roof(translation([index_2-len(line)/2,0.5,3-index_]),tex4))
            tiles.append(Floor(translation([index_2-len(line)/2,-0.5,3-index_]),tex5))
            bricks.append(vec3([index_2-len(line)/2,0,3-index_]))
            textures.append("jellyfish.png")
            index_2+=1
    index_+=1
textures=ImageTextureArray(textures)
prog = Program("vs.txt","fs.txt")

prog.use()
prog.setUniform("bboard",0.0)
prog.setUniform("instance",0)
cam = Camera()

glClearColor(0.2,0.4,0.6,1.0)

#glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)

keys=set()
last=sdl2.SDL_GetTicks()
paused=False
ev=sdl2.SDL_Event()
acel=0
acel2=0
TWOPI = 2.0*3.14159265358979323
angle=0
while 1:
    while 1:
        #print(len(bullets))
        #if len(bullets)>0:
            #print(bullets[0])
        if not sdl2.SDL_PollEvent(byref(ev)):
            break
    
        if ev.type == sdl2.SDL_QUIT:
            sys.exit(0)
        elif ev.type == sdl2.SDL_KEYDOWN:
            k = ev.key.keysym.sym
            keys.add(k)
            if k == SDLK_q:
                
                sdl2.SDL_Quit()
                sys.exit(0)
        elif ev.type == sdl2.SDL_KEYUP:
            k = ev.key.keysym.sym
            keys.discard(k)
        elif ev.type == sdl2.SDL_MOUSEBUTTONDOWN:
            #print("mouse down:",ev.button.button,ev.button.x,ev.button.y)
            bullets.append(cam.eye.xyz)
            vel.append(cam.W.xyz)
            life.append(time.time()+5)
            
        elif ev.type == sdl2.SDL_MOUSEBUTTONUP:
            #print("mouse up:",ev.button.button,ev.button.x,ev.button.y)
            pass
        elif ev.type == sdl2.SDL_MOUSEMOTION:
            #print("mouse mot:",ev.motion.xrel,ev.motion.yrel)
            acel=-ev.motion.xrel
            
        
            
    now = sdl2.SDL_GetTicks()
    elapsed = now-last
    last=now 

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBlendEquation( GL_FUNC_ADD )
    

    angle += 0.001*elapsed 
    if angle > TWOPI:
        angle -= TWOPI
    
    prog.setUniform("worldMatrix",worldMatrix)
    camPos=vec3(cam.eye[0],cam.eye[1],cam.eye[2])
    prog.setUniform("camPos",camPos)
    
    cam.turn(acel*0.01)
    if SDLK_w in keys:
        
        cam.walk(0.03)
    if SDLK_s in keys:
        cam.walk(-0.03)
    if SDLK_SPACE in keys and time.time()>=jump_time:
        jump=True
        cam.jump(0.4)
        fall_time=time.time()+0.1
        jump_time=time.time()+0.5
    if time.time()>=fall_time and jump==True:
        
        cam.fall(0.4)
        jump=False
    if SDLK_a in keys:
        cam.strafe(0.03)
    if SDLK_d in keys:
        cam.strafe(-0.03)
    
    prog.setUniform("lighting",1.0)
    prog.setUniform("bboard",0.5)
    prog.setUniform("instance",1.0)
    prog.setUniform("index",0)
    brick.draw(prog,bricks,textures)
    prog.setUniform("index",0)
    prog.setUniform("instance",0)
    prog.setUniform("bboard",0)

    for tile in tiles:
        
        tile.draw(prog)
    for robot in robots:
        for bull in bullets:
            dis=length(bull-robot.pos.xyz)
            
            if dis<=0.5:
                robot.timer=time.time()+1
                ind=bullets.index(bull)
                bullets.remove(bull)
                vel.remove(vel[ind])
                life.remove(life[ind])
        if robot.timer!=None:
            
            left=robot.alpha=(robot.timer-time.time())
            
            prog.setUniform("alpha",robot.alpha)
            if left<=0:
                robots.remove(robot)
        robot.draw(prog)
        prog.setUniform("alpha",1)

    prog.setUniform("bboard",1.0)
    prog.setUniform("lighting",0.0)
    
    
        
    #print(bricks)
    bullet.draw(prog,bullets,vel)
    for bull in bullets:
        ind=bullets.index(bull)
        death=life[ind]
        if time.time()>=death:
            
            bullets.remove(bullets[ind])
            vel.remove(vel[ind])
            life.remove(life[ind])
    prog.setUniform("bboard",0.0)
    prog.setUniform("lighting",0.0)
    angle+=0.01
    d=dot(cam.U,vec4([1,0,0,0]))
    gun.draw(prog)
    
    
    gunMatrix=scaling([0.25,0.25,0.25])*axisRotation(vec3([1,0,0]),math.radians(90))*axisRotation(vec3([0,1,0]),math.radians(180))*translation([0.2,0,-0.5])
    if d<-1:
        d=-1
    if d>1:
        d=1
    d=math.acos(d)
    if cam.W[0]<0:
        gunMatrix*=axisRotation(vec3([0,1,0]),-d)
    elif cam.W[0]>0:
        gunMatrix*=axisRotation(vec3([0,1,0]),d)
    else:
        gunMatrix*=axisRotation(vec3([0,1,0]),0)
    gunMatrix*=translation([cam.eye[0],cam.eye[1],cam.eye[2]])
    gun.worldMatrix=gunMatrix
    
    
    
    acel=0
    prog.setUniform("light.position",vec3(cam.eye[0],cam.eye[1],cam.eye[2]))    
    prog.setUniform("light.color", vec3(1,1,1))
    
    cam.draw(prog)
    sdl2.SDL_GL_SwapWindow(win)

