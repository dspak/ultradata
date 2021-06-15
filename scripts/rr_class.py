# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 08:45:04 2018

@author: adam
"""

import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

class ultraAnalysis():
    def __init__(self,name,fname):
        self.name = name
        self.fname = fname
        self.predictedFin = None

        with open(self.fname,'rb') as fid:
            self.data=fid.readlines()
        
        self.times = self.parseResults()
    
    def parseResults(self):
        times=[]
        for entry in self.data:
            m=re.search(r'(\d{1,2}):',str(entry))
            if m:
                if len(m.group(1))==1:
                    times.append(((int(m.group(1))*60) + int(entry[m.start(1)+2:m.start(1)+4])) / 60.0)
                else:
                    times.append(((int(m.group(1))*60) + int(entry[m.start(1)+3:m.start(1)+5])) / 60.0)
        return times

    def plotResults(self,k):
        #k=kind of plot: ['hist','line']
        df=pd.DataFrame(data=sorted(self.times))
        ax=plt.figure()
        ax=df.plot(kind=k,legend=None)
        ax.set_xlabel('total time (hours)')
        ax.set_title('{} total time'.format(self.name))
    
    def pFinish(self,p=[25,50,75]):
        self.predictedFin = np.percentile(self.times,p)
        print 'predicted finish times:'
        for xp,yp in zip(p,self.predictedFin):
            print 'top',xp,'percentile:',yp,'hours.'


    