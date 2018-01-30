import yaml
import os
from string import Template

def getYamlFile(f):
    with open(f, 'r') as stream:
        try:
            d = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit()
    return d

def checkProjectDirs(d):
    src=os.path.join(d['Path'],d['SourceSubPath'])                               
    tst=os.path.join(d['Path'],d['TestsSubPath'])                                
    if not os.path.exists(d['Path']):                                            
        os.makedirs(d['Path'])                                                      
    if not os.path.exists(src):                                             
        os.makedirs(src)                                                      
    if not os.path.exists(tst):                                             
        os.makedirs(tst)                                                      

def loadSourceFiles(d):
    m=""
    e={}

    mfn=d['MainFileName']                                                  
    mfloc=os.path.join(d['Path'],d['MainFileSubPath'],mfn)                 
                                                                           
    if not os.path.exists(mfloc):                                          
        open(mfloc,'a').close()                                              

    return (m,e)

projects = getYamlFile("Projects.yaml")
encoders = getYamlFile("Encoders.yaml")
languages = getYamlFile("Languages.yaml")

for p in projects.items():
    d=p[1] 

    checkProjectDirs(d)
    m, e = loadSourceFiles(d)


#    fl=open(mfloc).readline().rstrip()



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
