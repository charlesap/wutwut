import yaml
import os
from string import Template
from subprocess import call

def getYamlFile(f):
    with open(f, 'r') as stream:
        try:
            d = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit()
    return d

def FLSkipSpaces(s,c):
    while c<len(s) and s[c]==' ':
        c=c+1
    return c

def FLGetDirName(s,c):
    b=c
    while s[c].isalnum() and c<len(s)-1:
        c=c+1
    if s[c]=='(':
        c=c+1
    else:
        c=len(s)
    return s[b:c-1],c

def FLGetFileEntry(s,c):
    b=c
    while s[c]!=']' and c<len(s)-1:
        c=c+1
    if s[c]==']':
        c=c+1
    else:
        c=len(s)
    return s[b+1:c-1],c

def assemblepath(pth,nm):
    p=""
    for d in pth:
      p=p+d
      p=p+"/"
    return p+nm


def printpath(flist,pth,f):
    nm,tp=f.split(":")
    if '<' in nm and '>' in nm:
      b = nm.index('<')
      e = nm.index('>')
      if e - b > 2:
        pre=nm[0:b]
        vnm=nm[b+1:e]
        post=nm[e+1:]
        if vnm=='encoder':
          for i in encoders.items():
            ei=i[0]
            if ei[0]!='_':
              lnm=pre+ei+post
              flist.append([assemblepath(pth,lnm),None,None])
    else:
      flist.append([assemblepath(pth,nm),None,None])
    return flist

def FileList(r,s):
    ok=False
    flist=[]
    pth=[r]
    
    if len(s)>0:
      ok=True
      c=0
      
      while c<len(s):
        c = FLSkipSpaces(s,c)

        if s[c].isalpha():
          nm,c=FLGetDirName(s,c)
          pth.append(nm)
          c=FLSkipSpaces(s,c)

        elif s[c]=='[':
          f,c=FLGetFileEntry(s,c)
          flist=printpath(flist,pth,f)
          c=FLSkipSpaces(s,c)

        elif s[c]==')':
          c=c+1
          pth.pop()
          c=FLSkipSpaces(s,c)
         	
         
        else:
          print("uh... >"+s[c]+"<")
          print(" ERROR: Can't interpret "+d['Language']+ " SourceFiles string in Projects.yaml")
          c=len(s)
          ok=False

    return flist,ok

def LoadAll(fl):
    i=0
    e=len(fl)
    while i < e:
      fe=fl[i]
      p=os.path.dirname(fe[0])
      if not os.path.exists(p):
        os.makedirs(p)
        print("making "+p)
      if not os.path.exists(fe[0]):
        open(fe[0],'a').close()
        print("making "+fe[0])

      with open(fe[0]) as fh:  
        fl[i][2] = fh.read() 

      i=i+1
    return fl,True

def GenerateAll(fl):
    return fl,True

def MergeAll(fl):
    return fl,True

def WriteAll(fl):
    return fl,True

def BuildAll(fl):
    return fl,True

def TestAll(fl):
    return fl,True



projects = getYamlFile("Projects.yaml")
encoders = getYamlFile("Encoders.yaml")
languages = getYamlFile("Languages.yaml")


for p in projects.items():

    d=p[1] 
    l=languages[d['Language']]
    fl,ok=FileList(d['Path'],d['SourceFiles'])

    if ok:
      fl,ok=LoadAll(fl)
    if ok:
      fl,ok=GenerateAll(fl)
    if ok:
      fl,ok=MergeAll(fl)
    if ok:
      fl,ok=WriteAll(fl)
    if ok:
      fl,ok=BuildAll(fl)
    if ok:
      fl,ok=TestAll(fl)

      
