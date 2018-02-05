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
    moddfn = Template(l['DefFileName']).substitute(en=d['MainModFileName'])                       
    modifn = Template(l['ImpFileName']).substitute(en=d['MainModFileName'])                       
    binfn = Template(l['ImpFileName']).substitute(en=d['MainBinFileName'])
    tstfn = Template(l['ImpFileName']).substitute(en=d['MainTestFileName'])
    checkTheFile(os.path.join(d['Path'],d['MainModFileSubPath'],modifn))
    if moddfn != "":
        checkTheFile(os.path.join(d['Path'],d['MainModFileSubPath'],moddfn))                                             
    checkTheFile(os.path.join(d['Path'],d['MainBinFileSubPath'],binfn))
    checkTheFile(os.path.join(d['Path'],d['TestsSubPath'],tstfn))
    for i in encoders.items():
      if i[0]!="_top_":
        enc=i[1]
        encdfn = Template(l['DefFileName']).substitute(en=i[0])
        encifn = Template(l['ImpFileName']).substitute(en=i[0])
        checkTheFile(os.path.join(d['Path'],d['MainModFileSubPath'],encifn))
        if encdfn != "":
          checkTheFile(os.path.join(d['Path'],d['MainModFileSubPath'],encdfn))

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
          tc.write( '    ' + Template(l['StructElement']).substitute(enm=c[0],etp=t) +'\n' )         
        tc.write(Template(l['StructEnd']).substitute(snm=cn)+'\n')

def updateDefRefs(fn,l,d,encl,enci):                                                                                      
    s=open(fn,'r').read()                                                                                              
                                                                                                                       
    with open(fn,'w') as tc:                                                                                           
        tc.write(s+'\n')                                                                                               
        
        for i in encl:
          if i[0]!="_top_":

            if l['HasImplicitImports'] == "No" or i[0] not in enci:
              print(enci[i[0]],"\n\n")

              if l['DefFileName']=="":
                t=Template(l['ImpFileName']).substitute(en=i[0])                  
              else:                                                                                     
                t=Template(l['DefFileName']).substitute(en=i[0])
              tc.write( Template(l['ImportElement']).substitute(inm=t) +'\n' )
                                                                                                                       
projects = getYamlFile("Projects.yaml")
encoders = getYamlFile("Encoders.yaml")
languages = getYamlFile("Languages.yaml")


for p in projects.items():

    d=p[1] 
    l=languages[d['Language']]

    checkProjectDirs(d)                                                                                 
    checkSourceFiles(d,l,encoders)

    licf=os.path.join(d['Path'],"LICENSE")
    moddfn = Template(l['DefFileName']).substitute(en=d['MainModFileName'])           
    modifn = Template(l['ImpFileName']).substitute(en=d['MainModFileName'])           
    moddfp=os.path.join(d['Path'],d['MainModFileSubPath'],moddfn)
    modifp=os.path.join(d['Path'],d['MainModFileSubPath'],modifn)

    binf=os.path.join(d['Path'],d['MainBinFileSubPath'],Template(l['ImpFileName']).substitute(en=d['MainBinFileName']))
    tstf=os.path.join(d['Path'],d['TestsSubPath'],Template(l['ImpFileName']).substitute(en=d['MainTestFileName']))

    updateTheLicense(licf)
    updateTopComment(modifp,l)
    updateTopComment(binf,l)
    updateTopComment(tstf,l)

    updateStartModule(modifp,l,d)

    if moddfn != "":
        updateTopComment(moddfp,l)                                                                             

    if l['HasImplicitImports'] == "No":
        if moddfn != "":
            updateDefRefs(moddfp,l,d,encoders.items(),encoders)
        else:
            updateDefRefs(modifp,l,d,encoders.items(),encoders)

    updateStartInitModule(modifp,l,d)
    updateEndInitModule(modifp,l,d)
    updateEndModule(modifp,l,d)

    updateImportMain(binf,l,d)
    updateStartMain(binf,l,d)
    updatePreambleMain(binf,l,d)                                                             
    updateEndMain(binf,l,d)                                                               

    for i in encoders.items():                                                        
      if i[0]!="_top_":
        enc=i[1]                                                                      
        encdfn = Template(l['DefFileName']).substitute(en=i[0])                    
        encifn = Template(l['ImpFileName']).substitute(en=i[0])                      
        updateTopComment(os.path.join(d['Path'],d['MainModFileSubPath'],encifn),l)
        if encdfn != "":
          updateTopComment(os.path.join(d['Path'],d['MainModFileSubPath'],encdfn),l)

        updateStartModule(os.path.join(d['Path'],d['MainModFileSubPath'],encifn),l,d)        

        if 'Imports' in enc:
            if encdfn == "":
              updateDefRefs(os.path.join(d['Path'],d['MainModFileSubPath'],encifn),l,d,enc['Imports'],encoders)
            else:
              updateDefRefs(os.path.join(d['Path'],d['MainModFileSubPath'],encdfn),l,d,enc['Imports'],encoders)

        if 'Contains' in enc:
          if encdfn == "":
            updateContains(os.path.join(d['Path'],d['MainModFileSubPath'],encifn),l,d,i[0],enc['Contains'])
          else:
            updateContains(os.path.join(d['Path'],d['MainModFileSubPath'],encdfn),l,d,i[0],enc['Contains'])


        updateEndModule(os.path.join(d['Path'],d['MainModFileSubPath'],encifn),l,d)





