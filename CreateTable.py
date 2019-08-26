import csv, os

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



def insertNumbers(corpus,occVocab,lemmaVocab, posVocab, posxVcab,formVocab, relVocab):
    for el in corpus:
        print(occVocab[ el[3]])








corpus=CreateTable()