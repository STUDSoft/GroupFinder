#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 19:03:50 2018

@author: roccodeb
"""

# importing required modules
from zipfile import ZipFile
import entity as e
import os
import re

# specifying the zip file name 
file_name = "Geolife Trajectories 1.3.zip"
userList = []
# opening the zip file in READ mode 
with ZipFile(file_name, 'r') as zipfile:
    # printing all the contents of the zip file 
    for elem in zipfile.infolist():
        filename = elem.filename
        # print("\t"+filename)
        if not (elem.is_dir()):
            # print("Directory")
            # else:
            filepath, filename = os.path.split(elem.filename)
            filepath, trajectory = os.path.split(filepath)
            filepath, user = os.path.split(filepath)
            if filename.endswith(".plt") and not (filename.startswith("._")):
                # print("\t"+user)
                curUserInList = None
                for itemUser in userList:
                    if itemUser.get_identifier() == user:
                        # esiste gia
                        curUserInList = itemUser
                if not curUserInList:
                    curUserInList = e.User(user)
                    userList.append(curUserInList)

                curFile = zipfile.open(elem.filename)

                # line 1.. 5 are useless in this dataset
                for i in range(5):
                    line = curFile.readline()
                line = curFile.readline()
                curFileName = re.sub('\.plt$', '', filename)
                pointList = []
                # count=0 #number of point
                while line:
                    line = curFile.readline()
                    line = line.decode('UTF-8')
                    if line:
                        # count +=1
                        latitudine, longitudine, zero, altitudine, date, dateS, timeS = line.split(",")
                        pointList.append(e.Point(latitudine, longitudine, date))

                # print("\tcount: {}".format(count))
                # print("\t\t"+curFileName+"\n")

                curUserInList.add_detection(e.Detection(curFileName, pointList))
                zipfile.close() # cambiare posizione di questa istruzione poichè da errore
            # elif filename.endswith("labels.txt"):
            # print("\t\tlables")
            # else:
            # print("not my file")
#
"""
for elem in userList:
    print(elem.get_identifier())
    for detection in elem.get_detectionlist():
        print(detection.get_timestamp())
        for point in detection.get_pointlist():
            print(point.get_latitude()+","+point.get_longitude()+","+point.get_timestamp())
"""
