# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 08:48:30 2018

@author: adam
"""

import os
from datetime import datetime, timedelta
import datetime as dt
import numpy as np
import pandas as pd
import gpxpy as gpx
import re
import matplotlib.pyplot as plt
import seaborn as sea
from fitparse import FitFile
import gzip
import shutil
import time

strava_data='/home/adam/data/strava/activities/'
strava_output = '/home/adam/data/strava/tmp/'

for f in os.listdir(strava_data):
    if f.split('.')[-1] == 'gz':
        outname = f.split('.')[0]+'.fit'
        with gzip.open(os.path.join(strava_data,f),"rb") as f_in, open(os.path.join(strava_output,outname),"wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

fit_fields = ['distance','altitude','speed','cadence','timestamp','position_lat','position_long']

idx = 0
skips=0
start = time.time()
filelist = os.listdir(strava_output)
matdf = pd.DataFrame()
start_daterange = datetime.strptime('2016-06-01','%Y-%m-%d')
for f in filelist:
    try:
        fitfile = FitFile(os.path.join(strava_output,f))
        record_dict = {}
        start_timestamp = 0
        df = pd.DataFrame()    
        cumu_gain = 0
        cumu_loss = 0
        for msg in fitfile.get_messages():
            msgs.append(msg)
            if 'record' in msg.name:
                if start_timestamp == 0:
                    start_timestamp = msg.get_value('timestamp')
                if start_timestamp < start_daterange:
                    skips+=1
                    continue
                else:
                    for field in fit_fields:
                        record_dict[field] = msg.get_value(field)
                    record_dict['elapsedsec'] = (record_dict['timestamp'] - start_timestamp).seconds 
                    record_dict['activity'] = f.split('.')[0]
                    if idx-1 in df.index:
                        record_dict['rolling_elev'] = record_dict['altitude'] - df.loc[idx-1]['altitude']
                        if record_dict['rolling_elev']>=0:
                            cumu_gain += record_dict['rolling_elev']
                        else:
                            cumu_loss += np.abs(record_dict['rolling_elev'])
                        
                        record_dict['cumu_gain'] = cumu_gain
                        record_dict['cumu_loss'] = cumu_loss
                    else:
                        record_dict['rolling_elev'] = 0
                        record_dict['cumu_gain'] = 0
                        record_dict['cumu_loss'] = 0
                    tmp = pd.DataFrame(record_dict,index=[idx])
                    idx+=1
                    df = pd.concat([df,tmp],0)
        if df.empty:
            continue
        else:
            matdf = pd.concat([matdf,df],0)
    except:
        print f
        print 'error'
matdf.sort_values(by='timestamp',inplace=True)
matdf.dropna(inplace=True)
matdf.index = np.arange(0,len(matdf),1)
print (time.time()-start)/60,'minutes'

matdf.to_csv('dataset0.csv')

##############################
matdf = pd.read_csv('/home/adam/data/dataset0.csv',index_col=0)
matdf['timestamp'] = pd.to_datetime(matdf['timestamp'])

precede_vars = pd.DataFrame()
for a in matdf['activity'].unique():
    subset = matdf.loc[matdf['activity'] == a]
    precede_sub = {}
    subsubset = matdf.loc[(matdf['timestamp']>=subset['timestamp'].min()-timedelta(days=7)) & (matdf['timestamp']<subset['timestamp'].min())]
    precede_sub['acts'] = len(subsubset['activity'].unique())
    dists=[]
    elevs=[]
    times=[]
    for aa in subsubset['activity'].unique():
        dists.append(subsubset.loc[subsubset['activity'] == aa]['distance'].max())
        elevs.append(subsubset.loc[subsubset['activity'] == aa]['cumu_gain'].max())
        times.append(subsubset.loc[subsubset['activity'] == aa]['elapsedsec'].max())
    precede_sub['dist'] = sum(dists)
    precede_sub['elevs'] = sum(elevs)
    precede_sub['times'] = sum(times)
    precede_vars = pd.concat([precede_vars, pd.DataFrame(precede_sub,index=[a])],0)

cmat = matdf
cmat = cmat.join(precede_vars,on='activity',how='right')
cmat['dayofweek'] = cmat['timestamp'].apply(lambda x: x.dayofweek)
cmat['hourofday'] = cmat['timestamp'].apply(lambda x: x.hour)
cmat['monthofyear'] = cmat['timestamp'].apply(lambda x: x.month)

long_acts = {}
for a in cmat['activity'].unique():
    subset = cmat.loc[cmat['activity'] == a]
    subsubset = matdf.loc[(cmat['timestamp']>=subset['timestamp'].min()-timedelta(days=90)) & (cmat['timestamp']<subset['timestamp'].min())]
    long_acts[a] = len(subsubset['activity'].unique())


cmat['longterma'] = cmat['activity'].apply(lambda x: long_acts[x])

rollingspeed=cmat['speed'].rolling(window=500).mean()
cmat['rollingspeed'] = q.to_frame()
cmat['rollingspeed'].fillna(method='bfill')