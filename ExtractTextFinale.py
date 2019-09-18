#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re,io,os ,sys,pandas as pd
from ufal.udpipe import Model,Pipeline,ProcessingError
def cleanline(line):
     line = re.sub('<p>|</p>|<html><meta charset="UTF-8">|</html>',"",line)
     line = re.sub("&lt;(P\d#\d+)&gt;","\g<1>",line)
     line = re.sub('&gt;','>',line)
     line = re.sub('&lt;',"<",line)
     line = re.sub('\[.+?\]',"",line)
     line = re.sub("<(P\d#\d+)>","\g<1>",line)
     line1 = re.findall("\{.*?\}",line)
     line = re.sub("\{.*?\}","",line)
     line= re.sub("<.+?>","",line)
     line = re.sub("(\w*\')(\w+)","\g<1> \g<2>",line)
     line = re.sub("(\w+\')(\w+)","\g<1> \g<2>",line)
     line = re.sub(" \' ","\' ",line)
     line = re.sub(r"\[|\]|\{|\}","",line)
     line = re.sub(r"\(inint\)","",line)
     line = re.sub(r"^ +","",line)
     line = re.sub("\n","",line)
     line = re.sub("(\w)([,:.!?;\-])","\g<1> \g<2>",line)
     line = re.sub("([,:.!?;\-])(\w)","\g<1> \g<2>",line)
     #line = re.sub("(\d)(\w)","\g<1> \g<2>",line)
     line = re.sub(r"\(.*?\)","",line)
     line = re.sub("    |   |  "," ",line)
     
     if type(line1)==list:
         for el in line1:
            el=re.sub("<p>|</p>","",el)
            el=re.sub("&lt;(P\d#\d+)&gt;","\g<1>",el)
            el=re.sub("&gt;",">",el)
            el=re.sub('&lt;',"<",el)
            el=re.sub('\[.*?\]',"",el)
            el=re.sub("<(P\d#\d+)>","\g<1>",el)
            line2 = re.findall("\{.*?\}",el)
            el=re.sub("\{|\}","",el)
            el=re.sub("<.*?>","",el)
            el=re.sub("(\w*\')(\w+)","\g<1> \g<2>",el)  
            el=re.sub("(\w+\')(\w+)","\g<1> \g<2>",el)
            el=re.sub(" \' ","\' ",el)
            el=re.sub("\[.+?\]","",el)
            el = re.sub(r"\[|\]|\{|\}","",el)
            el = re.sub(r"\(inint\)","",el)
            el = re.sub(r"^ +","",el)
            el = re.sub("\n","",el)
            el = re.sub("(\w)([,:.!?;\-])","\g<1> \g<2>",el)
            el = re.sub("([,:.!?;\-])(\w)","\g<1> \g<2>",el)
            #el = re.sub("(\d)(\w)","\g<1> \g<2>",el)
            el = re.sub(r"\(.*?\)","",el)
            el = re.sub("    |   |  "," ",el)
            if type(line2)==list:
                for e in line2:
                    e=re.sub("\{|\}","",e)
                    e=re.sub("<.*?>","",e)
                    e=re.sub("(\w*\')(\w+)","\g<1> \g<2>",e)  
                    e=re.sub("(\w+\')(\w+)","\g<1> \g<2>",e)
                    e=re.sub(" \' ","\' ",e)
                    e=re.sub("\[.+?\]","",e)
                    e = re.sub(r"\[|\]|\{|\}","",e)
                    e = re.sub(r"\(inint\)","",e)
                    e = re.sub(r"^ +","",e)
                    e = re.sub("\n","",e)
                    e = re.sub("(\w)([,:.!?;\-])","\g<1> \g<2>",e)
                    e = re.sub("([,:.!?;\-])(\w)","\g<1> \g<2>",e)
                    #e = re.sub("(\d)(\w)","\g<1> \g<2>",e)
                    e = re.sub(r"\(.*?\)","",e)
                    e = re.sub("    |   |  "," ",e)
                    line=line+"\n"+e+"\n"
            else: 
                if not(line2==[]):
                    line=line+"\n"+line2+"\n"
                line=line+"\n"+el
     else:
         line1=re.sub("^\{|^ \{","",line1)
         line2 = re.findall("\{.*?\}",line1)
         if type(line2)==list:
                for e in line2:
                    e=re.sub("\{|\}","",e)
                    e=re.sub("<.*?>","",e)
                    e=re.sub("(\w*\')(\w+)","\g<1> \g<2>",e)  
                    e=re.sub("(\w+\')(\w+)","\g<1> \g<2>",e)
                    e=re.sub(" \' ","\' ",e)
                    e=re.sub("\[.+?\]","",e)
                    line=line+"\n"+e+"\n"
         else: 
                if not(line2==[]):
                    line=line+"\n"+line2+"\n"
         line = line+"\n"+line1
     a=re.findall("P\d#\d+",line)
     if(type(a)==list and len(a)>1):
         for i in range(1,len(a)):
             line=re.sub(a[i],"\n"+a[i],line)
     if (line=="" or line=="\n" or line==" \n"):
         return ""
     return line
     
def cleanHtml(sourcepath,outpath):

    for filename in os.listdir(sourcepath):
         text = io.open(sourcepath+filename,"r", encoding="utf-8")
         miotesto= text.readlines()
         m=open(outpath+filename[:-4]+"txt","a")
         m.truncate(0)
         for line in miotesto:
            cleanlinea=cleanline(line)
            cleanlinea= re.sub("P\d#\d+\n|P\d#\d+ \n","",cleanlinea)
            if type(re.findall("P\d#\d*",line))==list:
                a=re.findall("P\d#\d*",line)
                for i in range(1,(len(a)-1)):
                    cleanlinea=re.sub(a[i],"\n"+a[i],cleanlinea)                     
            m.write(cleanlinea)
            m.write("\n")

def extractData(sourcepath):
    data=[]
    testo=[["idfile","idfrase","parl","frase"]]
    for filename in os.listdir(sourcepath):
         text = io.open(sourcepath+filename,"r", encoding="utf-8")
         miotesto= text.readlines()
         a=[]
         a.append(filename[:-4])
         b=[]
         inizio=0
         i=1
         for line in miotesto:
             if not(line ==[] or line=="" or line =="\n" or line==" " or line=="  "):
                 if inizio==0:
                    a.append(line)
                 if inizio==1:    
                    if(re.findall("P\d#\d*",line)==[] and not(b==[])):
                        ind=testo.index(b)
                        d=b[2]+" "+b[3] + " "+ line
                        c=[]
                        c.append(filename[:-4])
                        c.append(str(i))
                        r=re.findall("P\d#\d*",d)
                        #print (b[1])
                        c.append(b[2])
                        c.append(re.sub("P\d#\d*","",d))
                        if not(c[3]==[] or c[3]=="" or c[3]=="\n" or c[3]==" " or c[3]=="  " or c[3]=="\t" or c[3=="   "]):
                            testo.append(c)
                            i=i+1
                            testo.pop(ind)
                            b=c
                    else:
                        c=[]
                        c.append(filename[:-4])
                        c.append(str(i))
                        r=re.findall("P\d",line)
                        
                        #print (b)
                        #print(filename)
                        #print (r)
                        #print (line)
                        c.append(r[0])
                        c.append(re.sub("P\d#\d*","",line))
                        
                        if not(re.findall("\w", c[3])==[]):
                            b=c   
                            testo.append(c)
                            i=i+1
                 if not(re.findall("INIZIO",line)==[]):
                     inizio=1
                     
         data.append(a)
         
    for el in testo:
        if (re.findall("\w",el[3])==[]):
            testo.pop(testo.index(el))
    return testo, data

def udpipe(testo,modelpath):
    model = Model.load(modelpath)
    corpus=[]
    corpus.append(testo[0])
    if not model:
        sys.stderr.write("Cannot load model from file '%s'\n" % modelpath)
        sys.exit(1)
        sys.stderr.write('done\n')

    pipeline = Pipeline(model, "horizontal", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")
    error = ProcessingError()
    i=1
    for el in testo[1:]:
        processed=pipeline.process(el[3], error)
        c=[]
        c.append(el[0])
        c.append(i)
        c.append(el[2])
        i=i+1
        processed=re.sub("# newdoc|# newpar|# sent_id = \d","",processed)
        a=[]
        for el in processed.split("\n"):
            if el!="":
                a.append(el.split("\t"))                   
        c.append(a)
        corpus.append(c)
    return corpus

def extractMetadata(data):
    dati=[]
    dati.insert(0,["idparl","idfile", "parl","sex","age","bcity","rcity","studies","job"])
    h=1
    for el in data:
        cont=0
        a=[]
        a.append(el[0])
        a.append(el[2])
        
        for e in el[4:]:
            if not(re.findall("Situazione",e)==[]):
                cont=1
            if cont==0:
                b=[]
                b.append(h)
                b.append(el[0])
                for ed in e.split(";"):
                    ed=re.sub(".*(P\d).*","\g<1>",ed)
                    ed=re.sub("\n","",ed)
                    ed=re.sub("\.","",ed)
                    ed=re.sub("sesso|età|età |anni| anni|nato ad|nata ad|nato a|nata a|luogo di nascita|e residenza|luogo di nascita e residenza|luogo di residenza|residente a ","",ed,flags=re.IGNORECASE)
                    ed=re.sub("femmina|donna","F",ed,flags=re.IGNORECASE)
                    ed=re.sub("maschio|uomo","M",ed,flags=re.IGNORECASE)
                    ed=re.sub("^ |^  |^   ","",ed)
                    ed=re.sub("savona","Savona",ed,flags=re.IGNORECASE)
                    ed=re.sub("torino","Torino",ed,flags=re.IGNORECASE)
                    ed=re.sub("avellino","Avellino",ed,flags=re.IGNORECASE)
                    ed=re.sub("imperia","Imperia",ed,flags=re.IGNORECASE)
                    ed=re.sub("^e | e ","",ed,flags=re.IGNORECASE)
                    ed=re.sub("^o | o ","",ed,flags=re.IGNORECASE)
                    ed=re.sub("^ |^  |^   ","",ed)
                    if (ed=="" or ed==" "):
                        ed="Sconosciuto"
                    b.append(ed)
                for i in range(len(b),8):
                    b.append("Sconosciuto")
                dati.append(b)
                h+=1
    return dati

def createTable(corpus,dati):
    cc=[]
    cc.append(["idfile","idfrase","idparl","nw","occurence","lemma","pos","posx","form","dep","rel","_","_2"])
    for el in corpus[1:]:
        
        for i in dati[1:]:
            if el[0]==i[1] and el[2]==i[2]:
                parl=int((i[0]))
        for e in el[3]:
            e.insert(0,el[0])
            e.insert(1,el[1])
            e.insert(2,parl)
            cc.append(e)
        
    return cc

def createdic(dic):
    i=1
    thisdic={}
    for el in dic:
        if el not in thisdic:
            thisdic[el]=i
            i=i+1
    return thisdic
def numerictable(cc):
    
    df=pd.DataFrame(cc)
    occurrenceVoc=createdic(list(sorted(set(df.loc[1:,4]))))
    lemmaVoc=createdic(list(sorted(set(df.loc[1:,5]))))
    posVoc=createdic(list(sorted(set(df.loc[1:,6]))))
    posxVoc=createdic(list(sorted(set(df.loc[1:,7]))))
    formVoc=createdic(list(sorted(set(df.loc[1:,8]))))
    relVoc=createdic(list(sorted(set(df.loc[1:,10]))))
    table=[]
    table.append(cc[0])
    for el in cc[1:]:
        el.insert(4,occurrenceVoc[el[4]])
        el.pop(5)
        el.insert(5,lemmaVoc[el[5]])
        el.pop(6)
        el.insert(6,posVoc[el[6]])
        el.pop(7)
        el.insert(7,posxVoc[el[7]])
        el.pop(8)
        el.insert(8,formVoc[el[8]])
        el.pop(9)
        el.insert(10,relVoc[el[10]])
        el.pop(11)
        table.append(el)
    return table
 
def writedic(dic,path):
    with open(path, 'w') as f:
        f.truncate(0)
        f.write("id\tentry\n")
        for key, value in dic.items():
            f.write(str(value) + "\t" +key+"\n")
def frasivoc(testo,dati):
    text=[]
    text.append(testo[0])
    for el in testo[1:]:
        for i in dati[1:]:
            if el[0]==i[1] and el[2]==i[2]:
                parl=(i[0])
        el.insert(2,parl)
        el.pop(3)
        text.append(el)
    return text
            
        
def main(sourcepath,outpath,modelpath)  :  
    print("Welcome!! \n")
    if (sourcepath[-1]!= "/"):
        sourcepath=sourcepath+"/"
    if (outpath[-1]!= "/"):
        outpath=outpath+"/"

    print("Cleaning and preparing data")
    cleanHtml(sourcepath,outpath)
    testo,data=extractData(outpath)
    print("Analyzing text with UdPipe Library")
    corpus= udpipe(testo,modelpath)
    print("Preparing Data Tables")
    dati=extractMetadata(data)
    cc=createTable(corpus,dati)
    df=pd.DataFrame(cc)
    occurrenceVoc=createdic(list(sorted(set(df.loc[1:,4]))))
    lemmaVoc=createdic(list(sorted(set(df.loc[1:,5]))))
    posVoc=createdic(list(sorted(set(df.loc[1:,6]))))
    posxVoc=createdic(list(sorted(set(df.loc[1:,7]))))
    formVoc=createdic(list(sorted(set(df.loc[1:,8]))))
    relVoc=createdic(list(sorted(set(df.loc[1:,10]))))
    table=numerictable(cc)
    "Writing Data Tables in .csv format separated by tab "
    writedic(occurrenceVoc,"occurrences.csv")
    writedic(lemmaVoc,"lemmi.csv")
    writedic(posVoc,"pos.csv")
    writedic(posxVoc,"posX.csv")
    writedic(formVoc,"formas.csv")
    writedic(relVoc,"rel.csv")
    finaltable=pd.DataFrame(table)
    frasiski=frasivoc(testo,dati)
    frasi=pd.DataFrame(frasiski)
    parlatori=pd.DataFrame(dati)
    frasi.to_csv("frasi.csv",sep="\t", header=False)
    finaltable.to_csv("finalTable.csv",sep="\t", header=False)
    parlatori.to_csv("parlatori.csv",sep="\t", header=False)
    sorted(set(finaltable.loc[1:,2]))
    print("Finished!!")
main(sys.argv[1],sys.argv[2],sys.argv[3])