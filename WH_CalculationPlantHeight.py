# -*- coding:utf-8 -*-

import os
import numpy as np
#使数组中的数全部显示
np.set_printoptions(threshold=np.inf)
#取消不影响结果的警告
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
import pandas as pd
import xlsxwriter
from math import sqrt
import time
start = time.perf_counter()

def CalcutionPlantHeightProcess(data_fun,threshold_down,threshold_top):
    #下面留下
    point_3layer_dic = {}
    zmin = data_fun.min(axis=0)[2]
    zmax = data_fun.max(axis=0)[2]
    threshold_down_fun = zmin+(zmax-zmin)*threshold_down
    data_down=[]
    z_down = []
    for i in range(len(data_fun)):
        if data_fun[i][2] <= threshold_down_fun:
            # print(data_r[i][2])
            d1 = data_fun[i]
            data_down.append(d1)
            z_down.append(data_fun[i][2])
    Point_data_down = np.array(data_down)
    point_3layer_dic['Point_data_down'] = Point_data_down
    #下面z值均值
    sum_down = 0
    for item in z_down:
        sum_down +=item
        meanZ_down = sum_down/len(z_down)
    #上面留下
    threshold_top_fun = zmin+(zmax-zmin)*threshold_top
    data_top=[]
    z_top = []
    for i in range(len(data_fun)):
        if data_fun[i][2] >= threshold_top_fun:
            d2 = data_fun[i]
            data_top.append(d2)
            z_top.append(data_fun[i][2])
    Point_data_top = np.array(data_top)
    point_3layer_dic['Point_data_top'] = Point_data_top
    #上面z值均值
    sum_top = 0
    for item in z_top:
        sum_top +=item
        meanZ_top = sum_top/len(z_top)
    #中间保留
    # data_middle = []
    # for i in range(len(data_fun)):
    #     if data_fun[i][2] > threshold_down_fun:
    #         if data_fun[i][2] < threshold_top_fun:
    #             d3 = data_fun[i]
    #             data_middle.append(d3)
    #             Point_data_middle = np.array(data_middle)
    #             point_3layer_dic['Point_data_middle'] = Point_data_middle
    Heightresult = meanZ_top-meanZ_down
    point_3layer_dic['Heightresult'] = Heightresult
    return point_3layer_dic

#测试一个
# Path = '2097_去噪_转换为ASCII.txt'
# testdata = np.loadtxt(Path,skiprows=1,dtype=float, delimiter=' ')
#
# result = CalcutionPlantHeightProcess(testdata,0.05,0.90)
# print(result)
# print(result['Heightresult'])
# np.savetxt("2097top.txt", result['Point_data_top'], fmt = '%f', delimiter = ' ')
# np.savetxt("2097down.txt", result['Point_data_down'], fmt = '%f', delimiter = ' ')
# np.savetxt("2097middle.txt", result['Point_data_middle'], fmt = '%f', delimiter = ' ')
# print('over')

#输入参数
Path = 'E:/2PaperandSomething/3MaizePaper/4MaizeEarHeight/20220816XX_XDZ_Map/UAV_LIDAR/0ForPlantHeight/2_SOR_result'

workbook = xlsxwriter.Workbook('Map_PH_AllPlots.xlsx')
worksheet = workbook.add_worksheet()

filelist = os.listdir(Path)
print(filelist)

for filename in filelist:
    filepath = os.path.join(Path, filename)
    print(filepath)
    name = filepath[108:112]
    data = np.loadtxt(filepath,skiprows=1,dtype=float, delimiter=' ')
    temp = CalcutionPlantHeightProcess(data, 0.05, 0.95)

    #export result
    #point cloud
    np.savetxt(name+"top.txt", temp['Point_data_top'], fmt = '%f', delimiter = ' ')
    np.savetxt(name+"down.txt", temp['Point_data_down'], fmt = '%f', delimiter = ' ')
    # np.savetxt(name+"middle.txt", temp['Point_data_middle'], fmt = '%f', delimiter = ' ')

    # height
    height = temp['Heightresult']
    worksheet.write(0, 0, 'name')
    worksheet.write(0, 1, 'PlantHeight')
    FileOrder = filelist.index(filename)
    worksheet.write(FileOrder + 1, 0, name)
    worksheet.write(FileOrder + 1, 1, round(height,2))

workbook.close()

#代码运行时间
end = time.perf_counter()
print('Running time: %s Seconds'%(end-start))
print("over")




























