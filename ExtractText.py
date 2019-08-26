# -*- coding: utf8 -*- #
"# -*- coding: utf-8 -*-"
import sys, io,re, os
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from ufal.udpipe import Model,Trainer, Pipeline, ProcessingError # pylint: disable=no-name-in-module
        

#############################################################
#                  START OF METHODS                         #
#############################################################




#############################################################
#                  CLEANLINE                                #       
#############################################################
def cleanLine(line):
    
        line = re.sub('<p>|</p>|<html><meta charset="UTF-8">|</html>',"",line)
        line = re.sub('&gt;','>',line)
        line = re.sub('&lt;',"<",line)
        line = re.sub('<+(P.*?)>+',"\g<1>",line)
        line = re.sub("<.*?>","",line)
        line1 = re.findall("\{.*?\}",line)
        line = re.sub('\{.*?\}',"",line)
        line = re.sub("\n","",line)
        line = re.sub(r"\[.*?\]","",line)
       # print (re.sub(r"\[.*?\]","",line))
        line = re.sub("(\w*\')(\w+)","\g<1> \g<2>",line)
       # line = re.sub(" ([{!?.,;:}])"," \g<1>",line)
        line = re.sub("(\w+\')(\w+)","\g<1> \g<2>",line)
        line = re.sub(" \' ","\' ",line)
        line = re.sub("([{!?.,;:}])"," \g<1>",line)
        line = re.sub("â\u0080¦","",line)
        line =re.sub(r"\[|\]|\{|\}","",line)
        line = re.sub(r"\(inint\)","",line)
        line = re.sub(r"^ +","",line)
        line = re.sub("\n","",line)
        if not(line1==[]):
            if  type(line1)==list:
                line=line.join("\n")         
                for el in line1:
                    el= re.sub("\{|\}","",el)
                    line=line+el 
               
            else:
                line1=re.sub("\{|\}","",line)
                line=line+line1    
           
        return line

#############################################################
#                  START OF CLASS                           #
#############################################################

class Text(object):


    

#############################################################
#               extractData                                 #
#############################################################

    def extractData(self,file):
        self.dati =[]
        self.testo =[]
        self.tokens=[]
        self.testoConTurni=[]
        # Apro il file
        text = io.open("/home/guido/Progetto Unitexto/textdata/txt/"+file,"r", encoding="utf-8")
        miotesto= text.readlines()
        # Creo le variabili interne all'oggetto dati contenente i metadati relativi a parlatori e testo
        # testo contenente le frasi 
        cont=0
        skip=0
        
        for line in miotesto:
            
            # elimino gli elementi indesiderati linea per linea e poi li attacco a dati e a line
            
            inizio = re.findall("INIZIO", line)
           
            if (cont==1 and skip==0 and re.match("</html>",line)==None):
                cleanline=cleanLine(line)
                try:
                    f=miotesto[miotesto.index(line)+1]
                    a=re.match(".*P\w\#\w+",f)
                except :
                    print("index probably out of range")
                if a==None and len(miotesto)>miotesto.index(line)+2:
                    cleanline= cleanline + cleanLine(f)
                    skip=skip+1
                    a=re.match("(P\w+?)",miotesto[miotesto.index(line)+2])
                    if a!=None:
                        cleanline= cleanline + cleanLine(miotesto[miotesto.index(line)+2])
                        skip=skip+1
                        a=re.match("(P\w+?)",miotesto[miotesto.index(line)+3])
                        if a!=None:
                            cleanline= cleanline + cleanLine(miotesto[miotesto.index(line)+3])
                            skip=skip+1
                            a=re.match("(P\w+?)",miotesto[miotesto.index(line)+4])
                            if a!=None:
                                cleanline= cleanline + cleanLine(miotesto[miotesto.index(line)+4])
                                skip=skip+1
                self.testoConTurni.append(cleanline)
                cleanline=re.sub("P\w\#\w+","",cleanline)
                self.testo.append(cleanline)
            if not(inizio==[]):
                    cont=1
            if (cont==0):
                self.dati.append(line)
            else:
                if skip>0:
                    skip-=1    



#############################################################
#               tokenizeText                                #
#############################################################




    def tokenizeText(self, testo, path):

        f= open(path, "a")
        for el in testo:
            el = re.sub('<(P\d#\d+)>',"\g<1>",el)
            el = re.sub("<.*>","",el)
            self.tokens.append(word_tokenize(el))
        for el in self.tokens:
            for e in el:
                if e=="'":
                    el[el.index(e)-1:el.index(e)+1]=["".join( el[el.index(e)-1:el.index(e)+1])]
                    f.write(e)
                else:
                    #a=re.match("\w+'\w+",e)
                    if re.match("\w+'\w+",e) != None: 
                        ind=el.index(e)
                        frst=re.search("\w+'",e).group(0)
                        scnd=re.search("'\w+",e).group(0)
                        scnd=re.sub("'","",scnd)   
                        #print(frst)  
                        f.write(frst)
                        f.write("\n")  
                        #print(scnd)     
                        f.write(scnd)
                        f.write("\n")    
                        el.insert(ind+1,frst)
                        el.insert(ind+2,scnd)
                        el.remove(e)
                    else:
                        f.write(e)
                        f.write("\n")
                       
            f.write("\n")
            

#############################################################
#                   extractMetadata                         #    
#############################################################
         


    def extractMetadata(self):                
        self.titolo=self.dati[1]
        self.parlatori=[]
        parl=0
        for el in self.dati:
            sit = re.findall("Situazione", el)
            a = re.findall("Parlatori",el)    
            if (sit!=[]):
                parl=0
            if (a!=[] or parl==1):
                parl=1
                self.parlatori.append(cleanLine(el))
           
                
            

                    
#############################################################
#                   cleanFolder                             #    
#############################################################


def cleanFolder(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)  
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
            
            
            
            
            

#############################################################
#                  udpipeG                                  #    
#############################################################
            
            
       
def udpipeG(pathmodel):
    path="/home/guido/Progetto Unitexto/textdata/cleanedTxt/"
    model = Model.load(pathmodel)
    if not model:
        sys.stderr.write("Cannot load model from file '%s'\n" % pathmodel)
        sys.exit(1)
        sys.stderr.write('done\n')

    pipeline = Pipeline(model, "horizontal", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")
    error = ProcessingError()
 #   corp = io.open("/home/guido/Progetto Unitexto/textdata/corpus.txt","r",encoding= "utf-8")
  # Read whole input
  #  string="".join(corp.readlines())
  
  # Process data
   # processed = pipeline.process(string, error)
   
    f = open("/home/guido/Progetto Unitexto/textdata/corpus.conllu", "a")
    f.truncate(0)
    i=1
    for filename in os.listdir(path):
        text=io.open(path+filename,"r", encoding="utf-8")
        string="".join(text.readlines())
        # Process data
        processed = pipeline.process(string, error)
        if error.occurred():
            sys.stderr.write("An error occurred when running run_udpipe: ")
            sys.stderr.write(error.message)
            sys.stderr.write("\n")
            sys.exit(1)
        f.write(processed)

        
        print ("File n " , i , " processed of ", len(os.listdir(path)))
        i+=1

#############################################################
#                  udpipeS                                  #    
#############################################################
            
            
       
def udpipeS(pathmodel,sourcepath, pathdestination):
    model = Model.load(pathmodel)
    if not model:
        sys.stderr.write("Cannot load model from file '%s'\n" % pathmodel)
        sys.exit(1)
        sys.stderr.write('done\n')

    pipeline = Pipeline(model, "horizontal", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")
    error = ProcessingError()

    i=1
    for filename in os.listdir(sourcepath):
        f = open(pathdestination+filename[:-3]+"conllu", "a")
        f.truncate(0)
       
        text=io.open(sourcepath+filename,"r", encoding="utf-8")
        string="".join(text.readlines())
        # Process data
        processed = pipeline.process(string, error)
        if error.occurred():
            sys.stderr.write("An error occurred when running run_udpipe: ")
            sys.stderr.write(error.message)
            sys.stderr.write("\n")
            sys.exit(1)
        f.write(processed)
        f.close()
        
        print ("File n " , i , " processed of ", len(os.listdir(sourcepath)))
        i+=1
        
        
        
#############################################################
#                  remove empytlines                        #
#############################################################
        
        
        
def removeEmptyLines(path):
      for filename in os.listdir(path): 
          with open(path+filename, "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                if i != "\n":
                    f.write(i)
            f.truncate()
            
            
            
#############################################################
#                  ExtractSentence                          #
#############################################################

def ExtractSentence(cleanedTurnspath):
    lista = []
    Parlatori = []

    for filename in os.listdir(cleanedTurnspath): 
        text = io.open(cleanedTurnspath+filename,"r", encoding="utf-8")
        miotesto= text.readlines()
        for line in miotesto:
            if (line!="" or line!=" "):
                speaker= (re.findall("P\d#\d+",line))
                parlatori= (re.findall("P\d#\d+",line))
                line = re.sub("P\d#\d+","",line)
                speaker.append(line)
                parlatori.append(filename)
                speaker.append(filename)
                lista.append(speaker)
                Parlatori.append(parlatori)
    return lista,Parlatori            
            



#############################################################
#                    END OF METHODS                         #
#############################################################



sourcepath = '/home/guido/Progetto Unitexto/textdata/txt'
metadatapath ="/home/guido/Progetto Unitexto/textdata/metadata/"
cleantextpath = "/home/guido/Progetto Unitexto/textdata/cleanedTxt/"
tokenizetextpath = "/home/guido/Progetto Unitexto/textdata/tokenizedTxt/"
cleanedTurnspath = "/home/guido/Progetto Unitexto/textdata/cleanedTxtWithTurns/"
modelpath = "/home/guido/Progetto Unitexto/UdPipe/udpipe-master/src/it_Guidomodel1.output"
conllupath = "/home/guido/Progetto Unitexto/textdata/conllu/"
cleanFolder(tokenizetextpath)
cleanFolder(metadatapath)
cleanFolder(cleantextpath)
cleanFolder(cleanedTurnspath)
cleanFolder(conllupath)
corpus=[]

print("Preparing and analizing text")
for filename in os.listdir(sourcepath):
    if filename[0]!=".":
        doc=Text()
        doc.extractData(filename)
        doc.extractMetadata()
        a = doc.testo
        for el in a[1:]:
            corpus.append(el)        
        doc.tokenizeText(doc.testo,tokenizetextpath+filename[:-4]+"tok")
        if filename[-3:]=="tml":
            
            m = open(metadatapath+filename[:-4]+"metadata", "a")
            f = open(cleantextpath+filename[:-4]+"txt","a")
            g = open(cleanedTurnspath+filename[:-4]+"txt","a")
        else:
            
            m = open(metadatapath+filename[:-3]+"metadata", "a")
            f = open(cleantextpath+filename[:-3]+"txt","a")
            g = open(cleanedTurnspath+filename[:-3]+"tok","a")
    
        for el in doc.testo:
            
            f.write (el)
            f.write ("\n")
        f.close()
        m.write(filename)
        m.write("\n")
        m.write(cleanLine(doc.titolo))
        m.write("\n")
        for el in doc.parlatori:
            m.write(el)
            m.write("\n") 
        m.close()
        for el in doc.testoConTurni:
            g.write(el)
            g.write ("\n")
 
corp = open ("/home/guido/Progetto Unitexto/textdata/corpus.txt","a")
corp.truncate(0)
for el in corpus:
    corp.write(el)
    corp.write(' ')
    corp.write("\n")
corp.close()   
udpipeS(modelpath,cleantextpath,conllupath)
removeEmptyLines(cleanedTurnspath)

sentenceList,parlatori=ExtractSentence(cleanedTurnspath)
aaa=0

          
   


#############################################################
#                                                        #
#############################################################








#############################################################
#                    END OF METHODS                         #
#############################################################
