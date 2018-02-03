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
    bin=os.path.join(d['Path'],d['MainBinFileSubPath'])
    if not os.path.exists(d['Path']):                                            
        os.makedirs(d['Path'])                                                      
    if not os.path.exists(src):                                             
        os.makedirs(src)                                                      
    if not os.path.exists(tst):                                             
        os.makedirs(tst)                                                      
    if not os.path.exists(bin):
        os.makedirs(bin)

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

def updateStartModule(fn,l,d):    
    s=open(fn,'r').read()
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['ModuleStart']).substitute(mn=d['MainModuleName'])+'\n')

def updateEndModule(fn,l,d):
    s=open(fn,'r').read()
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['ModuleEnd']).substitute(mn=d['MainModuleName'])+'\n' )

def updateStartInitModule(fn,l,d):                                                        
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:                                                          
        tc.write(s+'\n')                                                              
        tc.write( Template(l['ModuleInitStart']).substitute(mn=d['MainModuleName'])+'\n') 
                                                                                      
def updateEndInitModule(fn,l,d):                                                          
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:                                                          
        tc.write(s+'\n')                                                              
        tc.write( Template(l['ModuleInitEnd']).substitute(mn=d['MainModuleName'])+'\n' )  
                                                                                      
def updateImportMain(fn,l,d):                                                          
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:                                                          
        tc.write(s+'\n')                                                              
        tc.write( Template(l['MainFuncImport']).substitute(mn=d['MainModuleName'])+'\n' )  
                                                                                      
def updateStartMain(fn,l,d):                                                          
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:                                                          
        tc.write(s+'\n')                                                              
        tc.write( Template(l['MainStart']).substitute(mn=d['MainModuleName'])+'\n' )  
                                                                                      
def updatePreambleMain(fn,l,d):                                                          
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['MainFuncPreamble']).substitute(mn=d['MainModuleName'])+'\n' ) 
                                                                                     
def updateEndMain(fn,l,d):                                                            
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:
        tc.write(s+'\n')                                                                                      
        tc.write( Template(l['MainEnd']).substitute(mn=d['MainModuleName'])+'\n' )
                                                                                           
def updateContains(fn,l,d,cn,cd):                                                                 
    s=open(fn,'r').read()  
                                                               
    with open(fn,'w') as tc:                                                               
        tc.write(s+'\n') 
        tc.write( Template(l['StructStart']).substitute(snm=cn)+'\n')
        for c in cd:  
          t=c[1]
          if c[1] in l['Typemap']:
             t=l['Typemap'][c[1]]                                                                
          tc.write( '    ' + c[0] + ' ' + t +'\n' )         
        tc.write(Template(l['StructEnd']).substitute(snm=cn)+'\n')

projects = getYamlFile("Projects.yaml")
encoders = getYamlFile("Encoders.yaml")
languages = getYamlFile("Languages.yaml")


for p in projects.items():

    d=p[1] 
    l=languages[d['Language']]

    checkProjectDirs(d)                                                                                 
    checkSourceFiles(d,l,encoders)

    licf=os.path.join(d['Path'],"LICENSE")
    modf=os.path.join(d['Path'],d['MainModFileSubPath'],d['MainModFileName'])
    binf=os.path.join(d['Path'],d['MainBinFileSubPath'],d['MainBinFileName'])
    tstf=os.path.join(d['Path'],d['TestsSubPath'],d['MainTestFileName'])

    updateTheLicense(licf)
    updateTopComment(modf,l)
    updateTopComment(binf,l)
    updateTopComment(tstf,l)

    updateStartModule(modf,l,d)
    updateStartInitModule(modf,l,d)
    updateEndInitModule(modf,l,d)
    updateEndModule(modf,l,d)

    updateImportMain(binf,l,d)
    updateStartMain(binf,l,d)
    updatePreambleMain(binf,l,d)                                                             
    updateEndMain(binf,l,d)                                                               

    for i in encoders.items():                                                        
        enc=i[1]                                                                      
        encfn = Template(l['EncoderFileName']).substitute(en=i[0])                    
        updateTopComment(os.path.join(d['Path'],d['MainModFileSubPath'],encfn),l)
        updateStartModule(os.path.join(d['Path'],d['MainModFileSubPath'],encfn),l,d)        
#        updateStartInitModule(os.path.join(d['Path'],d['MainModFileSubPath'],encfn),l,d)       
#        updateEndInitModule(os.path.join(d['Path'],d['MainModFileSubPath'],encfn),l,d)       
        if 'Contains' in enc:
          updateContains(os.path.join(d['Path'],d['MainModFileSubPath'],encfn),l,d,i[0],enc['Contains'])

        updateEndModule(os.path.join(d['Path'],d['MainModFileSubPath'],encfn),l,d)




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
