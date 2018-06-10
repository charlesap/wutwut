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

def SkipSpaces(s,c):
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
              flist.append([assemblepath(pth,lnm),ei,tp,None,None]) #ei was vnm
    else:
      flist.append([assemblepath(pth,nm),'_top_',tp,None,None]) # _top_ was None
    return flist

def FileList(r,s):
    ok=False
    flist=[]
    pth=[r]
    
    if len(s)>0:
      ok=True
      c=0
      
      while c<len(s):
        c = SkipSpaces(s,c)

        if s[c].isalpha():
          nm,c=FLGetDirName(s,c)
          pth.append(nm)
          c=SkipSpaces(s,c)

        elif s[c]=='[':
          f,c=FLGetFileEntry(s,c)
          flist=printpath(flist,pth,f)
          c=SkipSpaces(s,c)

        elif s[c]==')':
          c=c+1
          pth.pop()
          c=SkipSpaces(s,c)
         	
         
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
        fl[i][4] = fh.read() 

      i=i+1
    return fl,True


def FTGetTo(s,c,d):
    b=c
    while s[c]!=d and c<len(s)-1:
        c=c+1
    if s[c]==d:
        c=c+1
    else:
        c=len(s)
    return s[b+1:c-1],c



def GenerateAll(wt,fl,en):
    i=0
    e=len(fl)
    while i < e:
      s=wt[fl[i][2]]
      #z=wt[0] #fl[i][2]
      ok=False
      d=""

      if len(s)>0:
        ok=True
        c=0

        while c<len(s):
          c=SkipSpaces(s,c)

          if s[c]=='(':
            fp,c=FTGetTo(s,c,':')
            l=open(fp,'r').read()
            tp,c=FTGetTo(s,c-1,')')
            if tp=='Comment':
              tc=wt['Comment']
              for q in l.splitlines():
                d=d+tc+q+"\n"
            else:
              d=d+l
            c=SkipSpaces(s,c)

          elif s[c]=='[':
            fp,c=FTGetTo(s,c,':')
            tp,c=FTGetTo(s,c-1,']')
            if tp in wt:
              tps=wt[tp]
            else:
              tps=" ERROR: "+tp+" Not Found in Projects.yaml entry for "+wt['Language']

            if fp=='{encoder}':
              fp=fl[i][1]
              d=d+Template(tps).substitute(me=fp)+"\n"

            elif fp[0]=='<' and fp[-1]=='>':
              ne=fp[1:-1].split('/')
              if len(ne)==1:
                if ne[0]=='encoder':
                  for p in en:
                    if p[0][0]!='_':
                      d=d+Template(tps).substitute(me=p)+"\n"
              else:
                if ne[0]=='encoder':
                  w=en[fl[i][1]]
                  if ne[1] in w:
                    for x in w[ne[1]]: 
                      d=d+Template(tps).substitute(me=x)+"\n"

                #fp="REPEAT "+ne[0]+" "+ne[1]
                #d=d+Template(tps).substitute(me=fp)+"\n"
            else:
              d=d+Template(tps).substitute(me=fp)+"\n"

            c=SkipSpaces(s,c)

          elif s[c]=='<':
            fp,c=FTGetTo(s,c,'>')
            d=d+fp
            c=SkipSpaces(s,c)

          else:
            print("uh... >"+s[c]+"<")
            print(" ERROR: Can't interpret '"+s+ "' file content string in Projects.yaml")
            c=len(s)
            ok=False
      
      fl[i][3]=d
      
      if fl[i][3]!=None:
        if fl[i][2]!='License':
          print(fl[i][0]+":")
          print(fl[i][3])
      i=i+1
    return fl,True

def MergeAll(wt,fl):
    return fl,True

def WriteAll(wt,fl):
    return fl,True

def BuildAll(wt,fl):
    return fl,True

def TestAll(wt,fl):
    return fl,True



projects = getYamlFile("Projects.yaml")
encoders = getYamlFile("Encoders.yaml")
languages = getYamlFile("Languages.yaml")


for p in projects.items():
  if p[0]!="all":

    wt=p[1].copy()
    wt.update(projects['all'])
    l=languages[wt['Language']]
    fl,ok=FileList(wt['Path'],wt['SourceFiles'])
    print(wt['Language']+" "+wt['License'])
    if ok:
      fl,ok=LoadAll(fl)
    if ok:
      fl,ok=GenerateAll(wt,fl,encoders)
    if ok:
      fl,ok=MergeAll(wt,fl)
    if ok:
      fl,ok=WriteAll(wt,fl)
    if ok:
      fl,ok=BuildAll(wt,fl)
    if ok:
      fl,ok=TestAll(wt,fl)

      
