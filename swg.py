# -*- coding: utf-8 -*-


#import laspy
# import os
# import xlsxwriter
import numpy as np
#使数组中的数全部显示
np.set_printoptions(threshold=np.inf)
import pandas as pd

def Process(data,voxelstep):
    xmin = data.min(axis=0)[0]
    xmax = data.max(axis=0)[0]
    ymin = data.min(axis=0)[1]
    ymax = data.max(axis=0)[1]
    zmin = data.min(axis=0)[2]
    zmax = data.max(axis=0)[2]
    #计算点云数据长、宽、高三个方向的体素个数
    rows = np.ceil((xmax - xmin)/voxelstep)
    cols = np.ceil((ymax - ymin)/voxelstep)
    heis = np.ceil((zmax - zmin)/voxelstep)
    #每层体素个数
    one_layer=rows * cols
    
    #计算点云数据在x、y、z方向上的体素个数
    data[:,0] = np.ceil((data[:,0] - xmin)/voxelstep)  #Xoffset
    data[:,1] = np.ceil((data[:,1] - ymin)/voxelstep)
    data[:,2] = np.ceil((data[:,2] - zmin)/voxelstep)
    #data[:,2] = np.ceil((data[:,2] - zmin)/0.02)
    points = np.array(data[:,0:3])
    
    a = np.unique(points, axis=0)
    pts = pd.DataFrame(a, columns = ['Off_x','Off_y','Off_z'])#以表的结构显示
    #print(pts)
    groups_test = pts.groupby(pts['Off_z'])
    #print(groups_test)
    layers=groups_test.size()/one_layer
    LAI=sum(layers)*1.1
    s=pts.groupby('Off_z').size()
    LAD=[]
    for i in pts.groupby('Off_z').size():
        layer =(i*1/(rows*cols))*1.1
        LAD.append(layer)

    swg=(np.argmax(LAD)+1)*(zmax-zmin)/(s.shape[0])-vox/2
    LAI=np.sum(LAD)
    
    LAD_n = np.array(LAD,dtype=np.int32)
    h =[]
    for i in range(LAD_n.shape[0]):
        s1 = (i+1)*(zmax-zmin)/(s.shape[0])
        h.append(s1)
    result = np.array([swg,LAI,np.array(LAD),np.array(h)])
    del LAD,swg,h,LAI   
    return result


with open("result.txt",'w') as f:
    for m in ['A']:
        for n in range(0,20,1):
            with pd.ExcelWriter(r'C:\Users\Administrator\Desktop\LAD\result.xlsx') as writer:
                for vox in np.arange(0.01,0.05,0.01):#0.12
                    path = "2019 UAV chuli/"+m+str(n+1)+".txt"
                    data = np.loadtxt(path, dtype=float, delimiter=' ')
                    temp = np.empty((4,))
                    temp = Process(data,vox)
                    f.write(m+str(n+1)+"step="+str(vox)+'\t'+str(temp[0])+'\t'+str(temp[1])+'\t'+str(temp[2])+'\t'+str(temp[3])+'\n')
                    sheetname=str(vox)
                    pdtemp2=pd.DataFrame(temp[2])
                    pdtemp3=pd.DataFrame(temp[3])
                    pdtemp23=pd.concat([pdtemp2,pdtemp3],axis=1)
                    print(pdtemp23)
                    pdtemp23.to_excel(writer, sheet_name=sheetname)
                del data

'''
txt格式
文件名步长  swg   LAI   ll   h      
'''          
