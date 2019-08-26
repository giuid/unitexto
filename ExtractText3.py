# -*- coding: utf8 -*- #
"# -*- coding: utf-8 -*-"
import sys, io,re, os, csv
import numpy as np
import pandas as pd
#from nltk.tokenize import sent_tokenize, word_tokenize
from ufal.udpipe import Model,Pipeline, ProcessingError # pylint: disable=no-name-in-module
        

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
        line = re.sub("([{!?.,;:}])"," \g<1> ",line)
        line = re.sub("\d+(\w+)","\g<1>",line )
        line = re.sub("â\u0080¦","",line)
        line =re.sub(r"\[|\]|\{|\}","",line)
        line = re.sub(r"\(inint\)","",line)
        line = re.sub(r"^ +","",line)
        line = re.sub("\n","",line)
        line = re.sub(r"\(.*?\)","",line)

        if not(line1==[]):
            if  type(line1)==list:
                line=line.join("\n")         
                for el in line1:
                    el= re.sub("\{|\}","",el)
                    line=line+el 
               
            else:
                line1=re.sub("\{|\}","",line1)
                line1 = re.sub(r"\[.*?\]","",line1)
                line1 = re.sub(r"\(.*?\)","",line1)

                line1 = re.sub('\{.*?\}',"",line1)
                line1 = re.sub("\n","",line1)
                line1 = re.sub(r"\[.*?\]","",line1)
               # print (re.sub(r"\[.*?\]","",line))
                line1 = re.sub("(\w*\')(\w+)","\g<1> \g<2>",line1)
               # line = re.sub(" ([{!?.,;:}])"," \g<1>",line)
                line1 = re.sub("(\w+\')(\w+)","\g<1> \g<2>",line1)
                line1 = re.sub(" \' ","\' ",line1)
                line1 = re.sub("([{!?.,;:}])"," \g<1> ",line1)
                line1 = re.sub("â\u0080¦","",line1)
                line1 =re.sub(r"\[|\]|\{|\}","",line1)
                line1 = re.sub(r"\(inint\)","",line1)
                line1 = re.sub(r"^ +","",line1)
                line1 = re.sub("\n","",line1)
                line=line+" "+line1    
           
        return line

#############################################################
#                  START OF CLASS                           #
#############################################################

class Text(object):

    
#############################################################
#               extractData                                 #
#############################################################

    def extractdata(self,file):
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
        
        
        for line in miotesto:
            inizio = re.findall("INIZIO", line)
            if (cont==1):
                cleanline=cleanLine(line)
                if (re.findall(r"P\w\#\w+",line)==[]):
                    try:
                        linesinP=re.sub("P\d\#\d+","",cleanline)
                        if not(linesinP=="" or linesinP==" " or linesinP=="\n"):
                            self.testoConTurni.append(self.testoConTurni[-1]+(cleanline))
                            self.testoConTurni.pop(-2)         
                            self.testo.append(self.testo[-1]+(linesinP))
                            self.testo.pop(-2)
                    except:
                        print("index probably out of range")

                else:
                    a=re.match(r"P\d\#\d+ \w+", cleanline)
                    linesinP=re.sub("P\d\#\d+","",cleanline)
                    if not(a==None):
                        self.testoConTurni.append(cleanline)
                        cleanline=re.sub("P\d\#\d+","",cleanline)
                        self.testo.append(cleanline)
            if not(inizio==[]):
                cont=1
            if (cont==0):
                self.dati.append(line)

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
"""
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
    return lista,Parlatori    """        



def ExtractSentence(cleanedTurnspath):
    
    listone=[]
    for filename in os.listdir(cleanedTurnspath):
        i=1
        lista = []
        text = io.open(cleanedTurnspath+filename,"r", encoding="utf-8")
        miotesto= text.readlines()
        for line in miotesto:
            speaker=[]
            #speaker.append(re.sub("#\d+","",(re.findall("P\d#\d+",line)[0])))
            a=re.sub("#\d+","",(re.findall("P\d#\d+",line)[0]))
            line = re.sub("P\d#\d+","",line)
            speaker.append(line)
            speaker.insert(0,(filename[:-4]))
            speaker.insert(1,i)
            speaker.insert(2,a)
            i=i+1
            lista.append(speaker)
        listone.append(lista)
    return (listone)            





#############################################################
#                  writeVocs                                #
#############################################################




def writeVocs(lista):
    #m = open(file, "a")
    dic={}
    i=1
    for el in lista:
        dic[el] = i
        #m.write(str(i)+"\t"+str(el)+"\n")
        i=i+1
    return dic    





#############################################################
#                     tableVoc                              #
#############################################################





def tableVoc(): 
    #fields = ["Occurrence","Lemma","POS","POSX","Form"] 
    conllupath= "/home/guido/Progetto Unitexto/textdata/conllu/"
    corpus=[]
    rows = [] 
    for filename in os.listdir(conllupath):    
    # reading csv file
        rows=[]
        with open(conllupath+filename, 'r') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
          
            # extracting each data row one by one 
            for row in csvreader:
                try:
                    a=re.match("# .*",row[0])
                    if not(a!=None or row==[]):    
                       # print(row)
                        rows.append(row) 
                except:
                    print
            # get total number of rows 
            #print("Total no. of rows: %d"%(csvreader.line_num)) 
        for el in rows:
            a=el[0].split("\t")
            if (len(a)==10):
                corpus.append(a)
    
    occurrences=[]
    lemmas=[]
    pos=[]
    posx=[]
    form=[]
    dependency=[]
    relation=[]
    for el in corpus:
        occurrences.append(el[1])
        lemmas.append(el[2])
        pos.append(el[3])
        posx.append(el[4])
        form.append(el[5])
        dependency.append(el[6])
        relation.append(el[7])
    postot={'occurrence': occurrences, 'lemma': lemmas, 'pos':pos,'posx':posx,'form':form}
    #tot = {'occurrence': occurrences, 'lemma': lemmas, 'pos':pos,'posx':posx,'form':form,'dependency':dependency,'relation':relation}
    df1=pd.DataFrame(postot, columns=['occurrence','lemma','pos','posx','form'])
    df1.to_csv(path_or_buf="/home/guido/Progetto Unitexto/textdata/pos&lemmi.prova", sep="\t")
    df1.pos.value_counts()
    occVoc= sorted(set(occurrences))
    lemmaVoc=sorted(set(lemmas))
    posVoc = sorted(set(pos))
    posxVoc = sorted(set(posx))
    formVoc  = sorted(set(form))
    relVoc = sorted(set(relation))
    occVocab = writeVocs(occVoc)
    lemmaVocab = writeVocs(lemmaVoc)
    posVocab = writeVocs(posVoc)
    posxVocab = writeVocs(posxVoc)
    formVocab = writeVocs(formVoc)
    relVocab= writeVocs(relVoc)
    numbers = np.unique(occurrences, return_inverse=True)
    return occVocab,lemmaVocab, posVocab, posxVocab,formVocab, relVocab,numbers




#############################################################
#                    CreateTable                            #
#############################################################


def CreateTable():
    conllupath="/home/guido/Progetto Unitexto/textdata/conllu/" 
    corpus=[]
    for filename in os.listdir(conllupath):
        rows=[]
        
        with open(conllupath+filename, 'r') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile)
            for el in csvreader:
                rows.append(el) 
            
        for el in rows:
            a=el[0].split("\t")
            if (len(a)==11):
                a.insert(0,filename[:-7])
                corpus.append(a)
    return corpus           





#############################################################
#                    END OF METHODS                         #
#############################################################
    




def insertNumbers(corpus,occVocab,lemmaVocab, posVocab, posxVocab,formVocab, relVocab):
    for el in corpus:
        el.insert(3,(occVocab[el[3]]))
        el.pop(4)
        el.insert(4,(lemmaVocab[el[4]]))
        el.pop(5)
        el.insert(5,(posVocab[el[5]]))
        el.pop(6)
        el.insert(6,(posxVocab[el[6]]))
        el.pop(7)
        el.insert(7,(formVocab[el[7]]))
        el.pop(8)
        el.insert(9,(relVocab[el[9]]))
        el.pop(10)
    return corpus
        
        
 
    


#############################################################
#                    END OF METHODS                         #
#############################################################
    





def WriteVocOnFile(path, voc):    
    with open(path, 'w') as f:
        f.truncate(0)
        for key in voc.keys():
            f.write(str(voc[key])+"\t"+key+"\n")                 
        f.close()

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
temppath = "/home/guido/Progetto Unitexto/textdata/temp/"
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
        doc.extractdata(filename)
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
sentenceList=ExtractSentence(cleanedTurnspath)
occVocab,lemmaVocab, posVocab, posxVocab,formVocab, relVocab,numbers=tableVoc()

    
    
    
for filename in os.listdir(conllupath): 
    with open(conllupath+filename, "r+") as f:
        d = f.readlines()
        f.seek(0)
        i=0
        for el in d:
            a=re.match(r"# sent_id = \d+",el)
            if not(a==None):
                i=i+1
            f.write(str(i)+"\t"+el)
        f.truncate()

corpus=CreateTable()
corpus=insertNumbers(corpus,occVocab,lemmaVocab, posVocab, posxVocab,formVocab, relVocab)
f = open('/home/guido/Progetto Unitexto/textdata/corpusnumerico.csv', "a")
f.truncate(0)
f.close()
with open('/home/guido/Progetto Unitexto/textdata/corpusnumerico.csv', mode='w') as employee_file:
    
    employee_writer = csv.writer(employee_file, delimiter='\t')
    for el in corpus:
        employee_writer.writerow(el[:-2])
        
textpath="/home/guido/Progetto Unitexto/textdata/"
WriteVocOnFile(textpath+"OccurrenceVoc.csv",occVocab)   
WriteVocOnFile(textpath+"LemmaVoc.csv",lemmaVocab)
WriteVocOnFile(textpath+"PosVoc.csv",posVocab)
WriteVocOnFile(textpath+"PosxVoc.csv",posxVocab)
WriteVocOnFile(textpath+"FormVoc.csv",formVocab)
WriteVocOnFile(textpath+"RelVoc.csv",relVocab)
#############################################################
#                                                        #
#############################################################








#############################################################
#                    END OF METHODS                         #
#############################################################
