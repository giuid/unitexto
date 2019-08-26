#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 14:49:33 2019

@author: guido
"""
import os,re
path="/home/guido/Progetto Unitexto/textdata/conllu/"
for filename in os.listdir(path): 
          with open(path+filename, "r+") as f:
            d = f.readlines()
            f.seek(0)
            cont=0
            for i in d:
                if re.findall("# sent_id = \d+",i)!=[]:
                    cont=cont+1
                a=str(cont)+"\t"+i    
                if i != "\n":
                    f.write(a)
            f.truncate()
            
path="/home/guido/Progetto Unitexto/textdata/"
for filename in os.listdir(path): 
          with open(path+filename, "r+") as f:
            d = f.readlines()
            f.seek(0)
            cont=0
            for i in d:
                if re.findall("# sent_id = \d+",i)!=[]:
                    cont=cont+1
                a=str(cont)+"\t"+i    
                if i != "\n":
                    f.write(a)
            f.truncate()