import tkinter.filedialog
import sys
import array
if len(sys.argv)==1:
    infile=tkinter.filedialog.askopenfilename()
    
    if not infile:
        sys.exit()
else:
    
    infile=sys.argv[1]
outfile=infile.replace(".obj",".mesh")
vertexdata=[]
normaldata=[]
texdata=[]
triangles=[]
mtls={None:{"count":0}}
omtl=None
currmtl=None
fp=open(infile)
for line in fp:
    line=line.strip()
    if len(line)==0:
        pass
    elif line.startswith("#"):
        pass
    elif line.startswith("v "):
        lst=line.split()[1:]
        lst=[float(a) for a in lst]
        vertexdata.append(lst)
    elif line.startswith("vn "):
        lst=line.split()[1:]
        lst=[float(a) for a in lst]
        normaldata.append(lst)
    elif line.startswith("vt "):
        
        lst=line.split()[1:]
        lst=[float(a) for a in lst]
        texdata.append(lst)
    elif line.startswith("f "):
        lst=line.split()[1:]
        if len(lst)!=3:
            print("Non-Triangle")
        else:
            t=[]
            mtls[omtl]["count"]+=1
            
            for vspec in lst:
                vv=vspec.split("/")
                if len(vv)==1:
                    t.append((int(vv[0])-1,0,0))
                elif len(vv)==2:
                    t.append((int(vv[0])-1,int(vv[1])-1,0))
                else:
                    if len(vv[1])==0:
                        t.append((int(vv[0])-1,0,int(vv[2])-1))
                    else:
                        t.append((int(vv[0])-1,int(vv[1])-1,int(vv[2])-1))
                #print(t)
            triangles.append(t)
    elif line.startswith("mtllib"):
        
        mfp=open(line[7:])
        for line in mfp:
            line=line.strip()
            if len(line)==0:
                pass
            elif line[0]=="#":
                pass
            elif line.startswith("newmtl"):
                currmtl=line[7:]
                
                mtls[currmtl]={"count":0}
            else:
                lst=line.split(" ",1)
                mtls[currmtl][lst[0]]=lst[1]
            
    elif line.startswith("usemtl"):
        omtl=line[7:]

otl=[]
indexmap={}
tmp=[]

for t in triangles:
    for vi,ti,ni in t:
        key=(vi,ti,ni)
        if key not in indexmap:
            indexmap[key]=len(tmp)
            tmp.append(key)
        otl.append(indexmap[key])
ofp=open(outfile,"wb")
ofp.write(b"mesh_01\n")
ofp.write(('num_vertices '+str(len(tmp))+"\n").encode())
ofp.write(("num_triangles "+str(len(triangles))+"\n").encode())
maxC=0
maxmtl=None


for mname in mtls:
    
        c=mtls[mname]['count']
        
    
    
        if c>maxC:
            maxC=c
            maxmtl=mname
ofp.write(("texture_file "+mtls[maxmtl]["map_Kd"]+'\n').encode())
#print(tmp)

tmpv=[]
tmpt=[]
tmpn=[]
for vi,ti,ni in tmp:
    tmpv.append(vertexdata[vi][0])
    tmpv.append(vertexdata[vi][1])
    tmpv.append(vertexdata[vi][2])
    tmpt.append(texdata[ti][0])
    tmpt.append(texdata[ti][1])
    #tmpt.append(texdata[ti][2])
    tmpn.append(normaldata[ni][0])
    tmpn.append(normaldata[ni][1])
    tmpn.append(normaldata[ni][2])
#print(tmpv)
#print(tmpt)
#print(tmpn)
ofp.write(b"vertices\n")
ofp.write(array.array('f',tmpv).tobytes())
ofp.write(b'\n')
ofp.write(b"texcoords\n")
ofp.write(array.array('f',tmpt).tobytes())
ofp.write(b'\n')
ofp.write(b"normals\n")
ofp.write(array.array('f',tmpn).tobytes())
ofp.write(b'\n')
ofp.write(b"indices\n")
ofp.write(array.array('H',otl).tobytes())
ofp.write(b'\n')
ofp.write(b'end\n')
ofp.close()
print("Done!")
