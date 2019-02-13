# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 18:44:09 2019

@author: z
"""
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

birddata = pd.read_csv("bird_tracking.csv")
bird_names = pd.unique(birddata.bird_name)

#路线分析
plt.figure(figsize=(7,7))
for bird_name in bird_names:
    ix = birddata.bird_name == bird_name
    x , y = birddata.longitude[ix],birddata.latitude[ix]
    plt.plot(x,y,".",label = bird_name)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(loc="lower right")

#速度分析
plt.figure(figsize=(7,7))
speed = birddata.speed_2d[birddata.bird_name == "Eric"]
ind = np.isnan(speed)
plt.hist(speed[~ind],bins=np.linspace(0,30,20),density=True)
plt.xlabel("2D speed (m/s)")
plt.ylabel("Frequency")
#birddata.speed_2d.plot(kind="hist",range=(0,30))

#时间戳
timestamps = []
for time in birddata.date_time:
    timestamps.append(datetime.datetime.strptime(time[0:-3],"%Y-%m-%d %H:%M:%S"))
birddata["timestamp"] = pd.Series(timestamps,index=birddata.index)
times = birddata.timestamp[birddata.bird_name == "Eric"]
elapsed_time = [time - times[0] for time in times]
elapsed_days = np.array(elapsed_time)/datetime.timedelta(days=1)

#速度图
data = birddata[birddata.bird_name == "Eric"]
next_day = 1
inds = []
daily_mean_speed = []
for (i,t) in enumerate(elapsed_days):
    if t < next_day:
        inds.append(i)
    else:
        #计算平均速度
        daily_mean_speed.append(np.mean(data.speed_2d[inds]))
        next_day +=1
        inds = []
plt.figure(figsize=(8,6))
plt.plot(daily_mean_speed)
plt.xlabel("Day")
plt.ylabel("Mean Speed (m/s)");

#Cartopy地图模块使用
import cartopy.crs as ccrs
import cartopy.feature as cfeature

proj = ccrs.Mercator()

plt.figure(figsize=(10,10))
ax = plt.axes(projection=proj)
ax.set_extent((-25.0,20.0,52.0,10.0))
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

for name in bird_names:
	ix = birddata['bird_name'] == name
	x , y = birddata.longitude[ix],birddata.latitude[ix]
	ax.plot(x,y,'.',transform=ccrs.Geodetic(),label=name)
plt.legend(loc="upper left")
plt.show();

