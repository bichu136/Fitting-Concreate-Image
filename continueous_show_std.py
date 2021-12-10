import torch
import pickle
import datetime
import time
with open('checkpoint','rb') as f:
    means,std,velocity,_ = pickle.load(f)

means[:,0] = means[:,0]*2048
means[:,1] = means[:,1]*1453
means[:,2] = means[:,2]*2048
means[:,3] = means[:,3]*1453
means[:,4] = means[:,4]*2048
means[:,5] = means[:,5]*143
means[:,6] = means[:,6]*255
means[:,7] = means[:,7]*255
means[:,8] = means[:,8]*255
means[:,9] = means[:,9]*255

# std[:,0] = std[:,0]*2048
# std[:,1] = std[:,1]*1453
# std[:,2] = std[:,2]*2048
# std[:,3] = std[:,3]*1453
# std[:,4] = std[:,4]*2048
# std[:,5] = std[:,5]*1453
# std[:,6] = std[:,6]*255
# std[:,7] = std[:,7]*255
# std[:,8] = std[:,8]*255
# std[:,9] = std[:,9]*255

arr  =[]

_c = 0
t = ['x1','y1','x2','y2','x3','y3','r','g','b','a']
while True:
    c =0
    _01 = 0
    _02 = 0
    _03 = 0

    print('\x1bc')
    print(datetime.datetime.now())
    for i in range(len(std)):

        # if (std[i].int() ==0).all():
            pass
        # else:
            for j in range(len(std[i])):
                if j in [0,2,4]:
                    if std[i][j]<10/2048:
                        c+=1
                    if std[i][j]>0.5:
                        _c +=1
                elif j in [1,3,5]:
                    if std[i][j]<10/1453:
                        c+=1
                    if std[i][j]>0.5:
                        _c +=1
                else:
                    if std[i][j]<0.05:
                        c+=1
                    if std[i][j]<0.2:
                        _01 +=1
                    elif std[i][j]<0.3:
                        _02 +=1
                    elif std[i][j]<0.4:
                        _03+=1

                    

                    if std[i][j]>0.5:
                        _c +=1
                    
    # print(len(arr))
    print("percentage of convergence <0.05")
    print(c/(std.shape[0]*std.shape[1]))
    print("percentage <0.2")
    print(_01/(std.shape[0]*std.shape[1]))
    print("percentage <0.3")
    print(_02/(std.shape[0]*std.shape[1]))
    print("percentage <0.4")
    print(_03/(std.shape[0]*std.shape[1]))
    time.sleep(200)
    #print(std)
    # for i in range(len(std)):
    #     for j in range(len(std[i])):
    #         if std[i][j]<0:
    #             std[i][j] = -std[i][j]
                
    # checkpoint = (means,std)
    # with open('checkpoint','wb') as f:
    #     pickle.dump(checkpoint,f)
