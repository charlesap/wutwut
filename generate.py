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

def checkTheFile(fn):

    if not os.path.exists(fn):                            
        open(fn,'a').close()

def checkSourceFiles(d,l,encoders):

    checkTheFile(os.path.join(d['Path'],"LICENSE"))
    checkTheFile(os.path.join(d['Path'],d['MetaFileName']))
    checkTheFile(os.path.join(d['Path'],d['MainModFileSubPath'],d['MainModFileName']))                                             
    checkTheFile(os.path.join(d['Path'],d['MainBinFileSubPath'],d['MainBinFileName']))
    checkTheFile(os.path.join(d['Path'],d['TestsSubPath'],d['MainTestFileName']))
    for i in encoders.items():
        enc=i[1]
        encfn = Template(l['EncoderFileName']).substitute(en=i[0])
        checkTheFile(os.path.join(d['Path'],d['MainModFileSubPath'],encfn))

def updateTheLicense(fn):
    l=open('LICENSE','r').read()
    with open(fn,'w') as f:
      f.write(l)

def updateTopComment(fn,l):
    t=open('TOPCOMMENT','r').read()
    s=open(fn,'r').read()

#    if s=="":
    with open(fn,'w') as tc:                                                                 
        tc.write(l['Comment'] + " " + os.path.basename(fn) + '\n')
        for tl in t.split('\n'):
          tc.write(l['Comment'] + " " + tl + '\n')
        tc.write('\n')
      
#    else:
#      pass
#      tl=t.split('\n')
#      fl=f[1].split('\n')
#    return changed
    



projects = getYamlFile("Projects.yaml")
encoders = getYamlFile("Encoders.yaml")
languages = getYamlFile("Languages.yaml")


for p in projects.items():

    d=p[1] 
    l=languages[d['Language']]

    checkProjectDirs(d)                                                                                 
    checkSourceFiles(d,l,encoders)

    updateTheLicense(os.path.join(d['Path'],"LICENSE"))
    updateTopComment(os.path.join(d['Path'],d['MainModFileSubPath'],d['MainModFileName']),l)
    updateTopComment(os.path.join(d['Path'],d['MainBinFileSubPath'],d['MainBinFileName']),l)
    updateTopComment(os.path.join(d['Path'],d['TestsSubPath'],d['MainTestFileName']),l)
    for i in encoders.items():                                                        
        enc=i[1]                                                                      
        encfn = Template(l['EncoderFileName']).substitute(en=i[0])                    
        updateTopComment(os.path.join(d['Path'],d['MainModFileSubPath'],encfn),l)
        

#    fl=open(mfloc).readline().rstrip()


#    modstmt = Template(l['ModuleStart']).substitute(mn=d['MainModuleName'])
#    print(modstmt)
#    mainstmt = Template(l['MainStart']).substitute(mn=d['MainModuleName'])
#    print(mainstmt)                                                         
#    mainendstmt = Template(l['MainEnd']).substitute(mn=d['MainModuleName'])
#    print(mainendstmt)                                                         
#    modendstmt = Template(l['ModuleEnd']).substitute(mn=d['MainModuleName'])
#    print(modendstmt)                                                         


#for e in encoders.items():
#    print(e[0])
#    d=e[1]
