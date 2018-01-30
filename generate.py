import yaml
import os
from string import Template

with open("Projects.yaml", 'r') as stream:
    try:
        projects = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit()

with open("Encoders.yaml", 'r') as stream:
    try:                                  
        encoders = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc) 
        exit()                       

with open("Languages.yaml", 'r') as stream:
    try:                                  
        languages = yaml.load(stream)      
    except yaml.YAMLError as exc:         
        print(exc)                        
        exit()                      

for p in projects.items():
    print("\n\n---",p[0]) 
    d=p[1] 
    lang=d['Language']
    loc=d['Path']
    src=os.path.join(loc,d['SourceSubPath'])
    tst=os.path.join(loc,d['TestsSubPath'])
    if not os.path.exists(loc):
      os.makedirs(loc)
    if not os.path.exists(src):
      os.makedirs(src)
    if not os.path.exists(tst):
      os.makedirs(tst)
    mfn=d['MainFileName']
    mfloc=os.path.join(loc,d['MainFileSubPath'],mfn)
    if not os.path.exists(mfloc):
      print("-->",mfloc," does not exist.")
      open(mfloc,'a').close()
    fl=open(mfloc).readline().rstrip()
    l=languages[d['Language']]
    modstmt = Template(l['ModuleStart']).substitute(mn=d['MainModuleName'])
    print(modstmt)
    mainstmt = Template(l['MainStart']).substitute(mn=d['MainModuleName'])
    print(mainstmt)                                                         
    mainendstmt = Template(l['MainEnd']).substitute(mn=d['MainModuleName'])
    print(mainendstmt)                                                         
    modendstmt = Template(l['ModuleEnd']).substitute(mn=d['MainModuleName'])
    print(modendstmt)                                                         


#for e in encoders.items():
#    print(e[0])
#    d=e[1]
