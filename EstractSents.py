#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, io, re
def ExtractSentence():
    cleanedTurnspath = "/home/guido/Progetto Unitexto/textdata/cleanedTxtWithTurns/"
    listone=[]
    for filename in os.listdir(cleanedTurnspath):
        i=1
        lista = []
        text = io.open(cleanedTurnspath+filename,"r", encoding="utf-8")
        miotesto= text.readlines()
        for line in miotesto:
            speaker=[]
            #speaker.append(re.sub("#\d+","",(re.findall("P\d#\d+",line)[0])))
            b=i
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
            
Lista=ExtractSentence()
aa=0