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


def Interp(l,wt,fl,en):
    r=l
    a=l.find("<~")
    b=l.find(">:<")
    c=l.find("~>")
    if a>-1 and b>a and c>b:
      
      prel=l[0:a]
      oldt=l[a+2:b]
      lookup=l[b+3:c]
      postl=l[c+2:]

      conv=oldt
      if lookup in wt:
        llist=wt[lookup]
        lu=llist.split(' ')
        for i in lu:
          bp=i.split('/')
          if bp[0]==oldt:
            conv=bp[1]
      r=prel+conv+postl
    return r

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
                d=d+Interp(tc+q+"\n",wt,fl,en)
            else:
              d=d+Interp(l,wt,fl,en)
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
              d=d+Interp(Template(tps).substitute(me=fp)+"\n",wt,fl,en)

            elif fp[0]=='<' and fp[-1]=='>':
              ne=fp[1:-1].split('/')
              if len(ne)==1:
                if ne[0]=='encoder':
                  for p in en:
                    if p[0][0]!='_':
                      r=Template(tps).substitute(me=p)+"\n"
                      d=d+Interp(r,wt,fl,en)
              else:
                if ne[0]=='encoder':
                  w=en[fl[i][1]]
                  if ne[1] in w:
                    for x in w[ne[1]]:
                      tt=[None,None,None,None] 
                      if type(x)==list:
                        if len(x)>0:
                          tt[0]=x[0]
                        if len(x)>1:
                          tt[1]=x[1]
                        if len(x)>2:
                          tt[2]=x[2]
                        if len(x)>3:
                          tt[3]=x[3]
                      r=Template(tps).substitute(me=x,me_0=tt[0],me_1=tt[1],me_2=tt[2],me_3=tt[3])
                      d=d+Interp(r+"\n",wt,fl,en)
                else:
                  w=en[ne[0]]
                  if ne[1] in w:
                    for x in w[ne[1]]:
                      tt=[None,None,None,None]
                      if type(x)==list:
                        if len(x)>0:
                          tt[0]=x[0]
                        if len(x)>1:
                          tt[1]=x[1]
                        if len(x)>2:
                          tt[2]=x[2]
                        if len(x)>3:
                          tt[3]=x[3]
                      r=Template(tps).substitute(me=x,me_0=tt[0],me_1=tt[1],me_2=tt[2],me_3=tt[3])
                      d=d+Interp(r+"\n",wt,fl,en)

                  #fp="REPEAT "+ne[0]+" "+ne[1]
                  #d=d+Template(tps).substitute(me=fp)+"\n"
            else:
              tt=[None,None,None,None]
              if type(tps)==list:
                        if len(tps)>0:
                          tt[0]=tps[0]
                        if len(tps)>1:
                          tt[1]=tps[1]
                        if len(tps)>2:
                          tt[2]=tps[2]
                        if len(tps)>3:
                          tt[3]=tps[3]

              r=Template(tps).substitute(me=fp,me_0=tt[0],me_1=tt[1],me_2=tt[2],me_3=tt[3])+"\n"
              d=d+Interp(r,wt,fl,en)

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
      
      #if fl[i][3]!=None:
      #  if fl[i][2]!='License':
      #    print(fl[i][0]+":")
      #    print(fl[i][3])
      i=i+1
    return fl,True

def MergeAll(wt,fl):
    return fl,True

def WriteAll(wt,fl):
    i=0
    e=len(fl)
    while i < e:
      fe=fl[i]
      p=os.path.dirname(fe[0])

      with open(fe[0],'w') as fh:
        fh.write(fl[i][3])

      i=i+1
    return fl,True

def BuildAll(wt,fl):
  if wt['MakeClean']!="":
    print("calling: "+wt['MakeClean'])
    call(wt['MakeClean'],shell=True)
  if wt['MakeLib']!="":
    print("calling: "+wt['MakeLib'])
    call(wt['MakeLib'],shell=True)
  if wt['MakeBin']!="":
    print("calling: "+wt['MakeBin'])
    call(wt['MakeBin'],shell=True)
  if wt['MakeTest']!="":
    print(wt['MakeTest'])
    call(wt['MakeTest'],shell=True)
  return fl,True

def TestAll(wt,fl):
  if wt['DoTest']!="":
      print(wt['DoTest'])
      call(wt['DoTest'],shell=True)

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
    #print(wt['Language']+" "+wt['License'])
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

      
