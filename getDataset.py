#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 19:03:50 2018

@author: roccodeb
"""

# importing required modules
from zipfile import ZipFile
import os 

# specifying the zip file name 
file_name = "Geolife Trajectories 1.3.zip"

# opening the zip file in READ mode 
with ZipFile(file_name, 'r') as zip: 
    # printing all the contents of the zip file 
    for elem in zip.infolist():
        filename = elem.filename
        print("\t"+filename)
        if elem.is_dir():
            print("Directory")
        else:
            if filename.endswith(".plt"):
                filepath, filename = os.path.split(elem.filename)
                filepath, trajectory = os.path.split(filepath)
                filepath, user = os.path.split(filepath)
                print("\t"+user)
                curFile = zip.open(elem.filename)
                
                #line 1.. 5 are useless in this dataset
                line = curFile.readline()
                line = curFile.readline()
                line = curFile.readline()
                line = curFile.readline()
                line = curFile.readline()
                line = curFile.readline()
                
                count=0 #number of point
                while line:    
                    line = curFile.readline()
                    line = line.decode('UTF-8')
                    if(line):
                        count +=1
                        latitudine,longitudine,zero,altitudine,date,dateS,timeS= line.split(",")
                        
                print("\tcount: {}".format(count))
                print("\t\t"+filename)
                zip.close
            elif filename.endswith("labels.txt"):
                print("\t\tlables")
            else:
                print("not my file")
