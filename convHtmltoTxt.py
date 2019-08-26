# -*- coding: utf8 -*- #
import codecs, io, nltk, re, os, shutil
from nltk.tokenize import sent_tokenize, word_tokenize
from ufal.udpipe import Model,Trainer, Pipeline, ProcessingError # pylint: disable=no-name-in-module
        

#############################################################
#                  START OF METHODS                         #
#############################################################




class Text(object):
    def cleanText(self,file):
        self.dati =[]
        self.testo =[]
        self.tokens=[]
        # Apro il file
        text = io.open("/home/guido/Progetto Unitexto/textdata/txt/"+file,"r", encoding="utf-8")

        # Creo le variabili interne all'oggetto dati contenente i metadati relativi a parlatori e testo
        # testo contenente le frasi 
        cont=0
        i=1
        for line in text:
            # elimino gli elementi indesiderati linea per linea e poi li attacco a dati e a line
            line = re.sub('<p>|</p>|<html><meta charset="UTF-8">|</html>|',"",line)
            line =  re.sub('&gt;','>',line)
            line = re.sub('&lt;',"<",line)
            line = re.sub('<+(P.*?)>+',"\g<1>",line)
            #print (line)
            line = re.sub("<.*>","",line)
            line1 = re.findall("\{.*?\}",line)
           # line1 = re.sub("\{(.*?)\}","\1",line1) 
            line = re.sub('\{.*?\}',"",line)
            line = re.sub("\n","",line)
            line = re.sub("\[.+\]","",line)
            line = re.sub("(\w*\')(\w+)","\g<1> \g<2>",line)
            line = re.sub(" ([!?.,;:])","\g<1>",line)
            line = re.sub("(\w+\')(\w+)","\g<1> \g<2>",line)
            line = re.sub(" \' ","\' ",line)
            
            inizio = re.findall("INIZIO", line)
            if (cont==0):
                self.dati.append(line)
            if (cont==1):
                self.testo.append(line)
            if not(inizio==[]):
                    cont=1
            if not(line1==[]):             
                for el in line1:
                    el= el
                    el= re.sub("\{|\}","",el)
                    self.testo.append(el)
                 #   print(el)
                #print (line1)           
           # print ( u''.join(line).encode('utf-8'))



#############################################################
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
                        print(frst)  
                        f.write(frst)
                        f.write("\n")  
                        print(scnd)     
                        f.write(scnd)
                        f.write("\n")    
                        el.insert(ind+1,frst)
                        el.insert(ind+2,scnd)
                        el.remove(e)
                    else:
                        f.write(e)
                        f.write("\n")
                       
            f.write("\n\n")
            

#############################################################
#############################################################
         


    def extractMetadata(self):                
        self.titolo=self.dati[1]
        self.parlatori=[]
        for i in range(self.dati.index("Parlatori")+1,self.dati.index("Situazione")):
            el=self.dati[i]
            el= re.sub("P\d *= *","",el)
            el=el.split(",")
            a=[]
            for x in el:
                x = re.sub("^ *","",x)
                a.append(x)    
            self.parlatori.append(a)
        self.situazione =  self.dati[self.dati.index("Situazione")+1]
        self.contesto = self.dati[self.dati.index("Contesto")+1]
        self.topic = self.dati[self.dati.index("Topic")+1]
        self.text = [len(self.testo)]
        i=0
        #for el in self.testo:
            #self.text[i]=[]
            #self.text[i].append(re.findall("P\d", el))
            #self.text[i].append(re.search("#\d*",el))
            #self.text[i].append(re.search("(P\d#\d* )|(<.*>)|[.*]","",el))

                    

#############################################################
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
#                    END OF METHODS                         #
#############################################################



sourcepath = '/home/guido/Progetto Unitexto/textdata/txt'
metadatapath ="/home/guido/Progetto Unitexto/textdata/metadata/"
cleantextpath = "/home/guido/Progetto Unitexto/textdata/cleanedTxt/"
tokenizetextpath = "/home/guido/Progetto Unitexto/textdata/tokenizedTxt/"
cleanFolder(tokenizetextpath)
cleanFolder(metadatapath)
cleanFolder(cleantextpath)
for filename in os.listdir(sourcepath):
    doc=Text()
    doc.cleanText(filename)
    doc.tokenizeText(doc.testo,tokenizetextpath+filename[:-4]+"tok")
    if filename[-3:]=="tml":
        
        m = open(metadatapath+filename[:-4]+"metadata", "a")
        f = open(cleantextpath+filename[:-4]+"txt","a")
 #       g = open(tokenizetextpath+filename[:-4]+"tok","a")
    else:
        
        m = open(metadatapath+filename[:-3]+"metadata", "a")
        f = open(cleantextpath+filename[:-3]+"txt","a")
 #       g = open(tokenizetextpath+filename[:-3]+"tok","a")


    for el in doc.testo:
        
        f.write (el)
        f.write ("\n")
    f.close()
         





    for el in doc.dati:
        m.write(el),
        m.write(' ')
        m.write("\n") 
    m.close()

          
   
