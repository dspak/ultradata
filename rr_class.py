# -*- coding: utf-8 -*-
"""
Created on Wed May 17 22:10:35 2017

@author: adam
"""
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



class race_results():
    def __init__(self,name,fname,data_flag):
        self.name=name
        self.fname=fname
        
        def parse_time1(t):
            numhour=len(t.split(':')[0])
            m=re.search(r'(\d{%x}):'%numhour,str(t))
            if m:
                return ((int(m.group(1))*60) + int(t[m.start(1)+3:m.start(1)+5])) / 60.0 

  
        if data_flag== 'csv':
            data=pd.read_csv(fname,header=None)
            #identify which column contains timing data.  must have 1 digit followed by ':'
            timecol='flag'
            for x in data:
                m=re.search('(\d{1}):',str(data[x][2]))
                if m:
                    timecol=x
                    self.times=data[timecol].apply(parse_time1)
                    break
            if timecol=='flag':
                self.times='error'
                print 'couldnt find the data column with time data'


            
            
        elif data_flag=='txt':
            with open(fname,'r') as f:
                data=f.readlines()
            times=[]
            for x in data:
                if x[0].isdigit():
                    times.append((((int(x.split(':')[0])*60)+(int(x.split(':')[1]))) / 60.0))
            self.times=times  
    
    def plot_time(self,k):
        #k=kind of plot
        df=pd.DataFrame(data=sorted(self.times))
        ax=plt.figure()
        ax=df.plot(kind=k,legend=None)
        ax.set_xlabel('total time (hours)')
        ax.set_title('{} total time'.format(self.name))