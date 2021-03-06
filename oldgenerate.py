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

    checkTheFile(os.path.join(d['Path'],"../wutwut/rsc/LICENSE"))
    metafn = d['MetaFileName']
    moddfn = Template(l['DefFileName']).substitute(en=d['MainModFileName'])                       
    modifn = Template(l['ImpFileName']).substitute(en=d['MainModFileName'])                       
    binfn = Template(l['ImpFileName']).substitute(en=d['MainBinFileName'])
    bihfn = Template(l['DefFileName']).substitute(en=d['MainBinFileName'])
    tstfn = Template(l['ImpFileName']).substitute(en=d['MainTestFileName'])
    if metafn != "":
      checkTheFile(os.path.join(d['Path'],d['MetaFileName']))
      updateTheMeta(os.path.join(d['Path'],d['MetaFileName']),l)
    checkTheFile(os.path.join(d['Path'],d['MainModFileSubPath'],modifn))
    if moddfn != "":
        checkTheFile(os.path.join(d['Path'],d['MainModFileSubPath'],moddfn))                                             
        checkTheFile(os.path.join(d['Path'],d['MainBinFileSubPath'],bihfn))
    checkTheFile(os.path.join(d['Path'],d['MainBinFileSubPath'],binfn))
    checkTheFile(os.path.join(d['Path'],d['TestsSubPath'],tstfn))
    for i in encoders.items():
      if i[0]!="_top_" and i[0]!="_cmd_":
        enc=i[1]
        encdfn = Template(l['DefFileName']).substitute(en=i[0])
        encifn = l['ImpSubPrefix']+Template(l['ImpFileName']).substitute(en=i[0])
        checkTheFile(os.path.join(d['Path'],d['MainModFileSubPath'],encifn))
        if encdfn != "":
          checkTheFile(os.path.join(d['Path'],d['MainModFileSubPath'],encdfn))

def updateTheMeta(fn,l):
    c=l['MetaText']
    with open(fn,'w') as f:
      f.write(c)


def updateTheLicense(fn):
    l=open('../wutwut/rsc/LICENSE','r').read()
    with open(fn,'w') as f:
      f.write(l)

def updateTopComment(fn,l):
    t=open('../wutwut/rsc/TOPCOMMENT','r').read()
    s=open(fn,'r').read()

#    if s=="":
    with open(fn,'w') as tc:                                                                 
        tc.write(l['xComment'] + " " + os.path.basename(fn) + '\n')
        for tl in t.split('\n'):
          tc.write(l['xComment'] + " " + tl + '\n')
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
        tc.write( Template(l['xModuleStart']).substitute(mn=d['MainModuleName'])+'\n')

def updateEndModule(fn,l,d):
    s=open(fn,'r').read()
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['xModuleEnd']).substitute(mn=d['MainModuleName'])+'\n')

def updateGuardStart(fn,l,nm):                                                             
    s=open(fn,'r').read()                                                                  
    with open(fn,'w') as tc:                                                               
        tc.write(s+'\n')
        tc.write( Template(l['GuardStart']).substitute(gnm=nm)+'\n')      
                                                                                           
def updateGuardEnd(fn,l,nm):                                                               
    s=open(fn,'r').read()                                                                  
    with open(fn,'w') as tc:                                                                
        tc.write(s+'\n')                                                                    
        tc.write( Template(l['GuardEnd']).substitute(gnm=nm)+'\n' )
                                                                                            
def updateStartInitModule(fn,l,d,tmn):                                                        
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:                                                          
        tc.write(s+'\n')                                                              
        tc.write( Template(l['xModuleInitStart']).substitute(mn=tmn)+'\n') 
                                                                                     
def updateEndInitModule(fn,l,d,tmn):                                                          
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:                                                          
        tc.write(s+'\n')                                                              
        tc.write( Template(l['xModuleInitEnd']).substitute(mn=tmn)+'\n' )  
                                                                                      
def updateImportMain(fn,l,d):                                                          
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:                                                          
        tc.write(s+'\n')                                                              
        tc.write( Template(l['xMainFuncImport']).substitute(mn=d['MainModuleName'])+'\n' )  
                                                                                      
def updateStartMain(fn,l,d):                                                          
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:                                                          
        tc.write(s+'\n')                                                              
        tc.write( Template(l['xMainStart']).substitute(mn=d['MainModuleName'],bn=d['MainBinFileName'])+'\n' )  
                                                                                      
def updatePreMainStart(fn,l,d):
    s=open(fn,'r').read()
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['xMainPreStart']).substitute(mn=d['MainModuleName'],bn=d['MainBinFileName'])+'\n' )

def updatePostMainEnd(fn,l,d):
    s=open(fn,'r').read()
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['xMainPostEnd']).substitute(mn=d['MainModuleName'])+'\n' )

def updatePreambleMain(fn,l,d):                                                          
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['xMainFuncPreamble']).substitute(mn=d['MainModuleName'])+'\n' ) 
                                                                                     
def updateEndMain(fn,l,d):                                                            
    s=open(fn,'r').read()                                                             
    with open(fn,'w') as tc:
        tc.write(s+'\n')                                                                                      
        tc.write( Template(l['xMainEnd']).substitute(mn=d['MainModuleName'])+'\n' )
                                                                                           
def updateImportTest(fn,l,d):
    s=open(fn,'r').read()
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['xTestFuncImport']).substitute(mn=d['MainModuleName'])+'\n' )

def updateStartTest(fn,l,d):
    s=open(fn,'r').read()
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['xTestStart']).substitute(mn=d['MainModuleName'])+'\n' )

def updatePreambleTest(fn,l,d):
    s=open(fn,'r').read()
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['xTestFuncPreamble']).substitute(mn=d['MainModuleName'])+'\n' )

def updateEndTest(fn,l,d):
    s=open(fn,'r').read()
    with open(fn,'w') as tc:
        tc.write(s+'\n')
        tc.write( Template(l['xTestEnd']).substitute(mn=d['MainModuleName'])+'\n' )
 
def updateContains(fn,l,d,cn,cd):                                                                 
    s=open(fn,'r').read()  
                                                               
    with open(fn,'w') as tc:                                                               
        tc.write(s+'\n') 
        tc.write( Template(l['StructStart']).substitute(snm=cn)+'\n')
        for c in cd:  
          t=c[1]
          m=""
          if type(c[1]) is list:
            m=t[0]
            t=t[1]
          if t in l['Typemap']:
             t=l['Typemap'][c[1]]
          if type(c[1]) is list:
            tc.write( '    ' + Template(l['StructElementImported']).substitute(enm=c[0],em=m,etp=t) +'\n' )
          else:                                                                
            tc.write( '    ' + Template(l['StructElement']).substitute(enm=c[0],etp=t) +'\n' )         
        tc.write(Template(l['StructEnd']).substitute(snm=cn)+'\n')

def updateProvidesDef(fn,l,d,cn,cd):                                                                                      
    s=open(fn,'r').read()                                                                                              
                                                                                                                       
    with open(fn,'w') as tc:                                                                                           
        tc.write(s+'\n')                                                                                               
        

        for c in cd: 
         if c!=[]:                                                                                                  
          t=c[2]
          if c[2] in l['Typemap']:                                                         
             t=l['Typemap'][c[2]]
          prm=c[1]
          if prm==[]:
             prm=""
          else:
             prm=""
          tc.write( Template(l['FuncDef']).substitute(fnm=c[0],ftyp=t,fprm=prm) +'\n' )                           

def updateProvidesImp(fn,l,d,cn,cd):                                                                                   
    s=open(fn,'r').read()                                                                                              
                                                                                                                       
    with open(fn,'w') as tc:                                                                                           
        tc.write(s+'\n')                                                                                               
                                                                                                                       
        for c in cd:
         if c!=[]:
          print("--->"+str(c))                                                                                                   
          t=c[2]                                                                                                       
          if c[2] in l['Typemap']:                                                          
             t=l['Typemap'][c[2]]                                                           
          prm=c[1]
          if prm==[]:
             prm=""
          else:         
             prm=""
          tc.write(Template(l['FuncImpStart']).substitute(fnm=c[0],ftyp=t,fprm=prm) +'\n' )
          tc.write(Template(l['FuncImpEnd']).substitute(fnm=c[0],ftyp=t,fprm=prm) +'\n' )

                                                                                                                       
def updateDefRefs(fn,l,d,encl,enci,top):                                                                                      
    s=open(fn,'r').read()                                                                                              
                                                                                                                       
    with open(fn,'w') as tc:                                                                                           
        tc.write(s+'\n')                                                                                               
        
        for i in encl:
          if i[0]!="_top_" and i[0]!="_cmd_":

            if l['xHasImplicitImports'] == "No" or i[0] not in enci:

              if l['DefFileName']=="":
                t=Template(l['RefFileName']).substitute(en=i[0])                  
              else:                                                                                     
                t=Template(l['DefFileName']).substitute(en=i[0])
              tc.write( Template(l['ImportElement']).substitute(inm=l['ImpSubPrefix']+t,anm=t) +'\n' )
              if top:
                tc.write( Template(l['LinkElement']).substitute(inm=l['ImpSubPrefix']+t) +'\n' )
                                                                                                                       
projects = getYamlFile("Projects.yaml")
encoders = getYamlFile("Encoders.yaml")
languages = getYamlFile("Languages.yaml")


for p in projects.items():
 if p[0]!="all":
    d=p[1] 
    l=languages[d['Language']]

    checkProjectDirs(d)                                                                                 
    checkSourceFiles(d,l,encoders)

    licf=os.path.join(d['Path'],"../wutwut/rsc/LICENSE")

    binf=os.path.join(d['Path'],d['MainBinFileSubPath'],Template(l['ImpFileName']).substitute(en=d['MainBinFileName']))
    bihf=os.path.join(d['Path'],d['MainBinFileSubPath'],Template(l['DefFileName']).substitute(en=d['MainBinFileName']))
    tstf=os.path.join(d['Path'],d['TestsSubPath'],Template(l['ImpFileName']).substitute(en=d['MainTestFileName']))

    updateTheLicense(licf)
    updateTopComment(binf,l)
    if l['DefFileName'] != "":
       updateTopComment(bihf,l)
    updateTopComment(tstf,l)

    updateImportMain(binf,l,d)
    updatePreMainStart(binf,l,d)
    updateStartMain(binf,l,d)
    updatePreambleMain(binf,l,d)                                                             
    updateEndMain(binf,l,d)                                                               



    updateImportTest(tstf,l,d)
    updateStartTest(tstf,l,d)
    updatePreambleTest(tstf,l,d)
    updateEndTest(tstf,l,d)


    for i in encoders.items():
      encnm=i[0]
      if encnm=="_top_":
        encnm=d['MainModFileName']
      if encnm=="_cmd_":
        encnm=d['MainBinFileName']
      enc=i[1]                                                        
      if i[0]=="_top_":
        moddfn = Template(l['DefFileName']).substitute(en=d['MainModFileName'])                                            
        modifn = Template(l['ImpFileName']).substitute(en=d['MainModFileName'])                                            
      elif i[0]=="_cmd_":
        moddfn = Template(l['DefFileName']).substitute(en=d['MainBinFileName'])
        modifn = Template(l['ImpFileName']).substitute(en=d['MainBinFileName'])
      else:
        moddfn = Template(l['DefFileName']).substitute(en=i[0])                                                        
        modifn = l['ImpSubPrefix']+Template(l['ImpFileName']).substitute(en=i[0])                                                        

      if i[0]=="_cmd_":
        moddfp=os.path.join(d['Path'],d['MainBinFileSubPath'],moddfn)
        modifp=os.path.join(d['Path'],d['MainBinFileSubPath'],modifn)
      else:
        moddfp=os.path.join(d['Path'],d['MainModFileSubPath'],moddfn)                                                      
        modifp=os.path.join(d['Path'],d['MainModFileSubPath'],modifn)                                                      

      if i[0]!="_cmd_":
        updateTopComment(modifp,l)                                                                                         
        updateStartModule(modifp,l,d)
                                                                                      
        if moddfn != "":                                                                                                   
          updateTopComment(moddfp,l)                                                                                     
          updateGuardStart(moddfp,l,encnm)

      if i[0]=="_top_":                                                                                                                      
        if l['xHasImplicitImports'] == "No":                                                                                
            if moddfn != "":                                                                                               
                updateDefRefs(moddfp,l,d,encoders.items(),encoders,True)                                                        
            else:                                                                                                          
                updateDefRefs(modifp,l,d,encoders.items(),encoders,True)                                                        

      elif i[0]=="_cmd_":
        pass

      else:                       
                                                                                               
        updateStartInitModule(modifp,l,d,i[0])                                                                             
                                                                                  
        if 'Imports' in enc:                                                                                           
            if moddfn == "":                                                                                           
              updateDefRefs(modifp,l,d,enc['Imports'],encoders,False)        
            else:                                                                                                      
              updateDefRefs(moddfp,l,d,enc['Imports'],encoders,False)        
                                                                                                                       
        if 'Contains' in enc:                                                                                          
          if moddfn == "":                                                                                             
            updateContains(modifp,l,d,i[0],enc['Contains'])            
          else:                                                                                                        
            updateContains(moddfp,l,d,i[0],enc['Contains'])            

      if 'Provides' in enc:
          if l['DefFileName'] != "":                                                                                             
            updateProvidesDef(moddfp,l,d,i[0],enc['Provides'])
          updateProvidesImp(modifp,l,d,i[0],enc['Provides'])

      if i[0]!="_top_" and i[0]!="_cmd_":                                                                                                                                                                                               
          updateEndInitModule(modifp,l,d,i[0])                                                                                    
         

      if i[0]!="_cmd_":
        updateEndModule(modifp,l,d)                                                                                        

      if moddfn != "":
          updateGuardEnd(moddfp,l,encnm)                                                                                   

    updatePostMainEnd(binf,l,d)

    if d['MakeLib'] != "":
        print("calling: "+d['MakeLib'])
        call(d['MakeLib'],shell=True)

    if d['MakeBin'] != "":
        print("calling: "+d['MakeBin'])
        call(d['MakeBin'],shell=True)


