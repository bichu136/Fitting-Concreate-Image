
import numpy as np
import cv2
import time
from util import *
import multiprocessing
import sys
import asyncio
from PIL import Image, ImageDraw
f=open('render_log.txt','w')
async def create_point(x,y,height,width):
    if x>1:
        x=1
    if y>1:
        y=1
    
    _x = int(x*width)
    _y = int(y*height)
    return _x,_y
async def create_number(x,cap=1,t = "int"):
    if x>1:
        x=1
    if t == "int":
        r =  int(x*cap)
    else:
        r = float(x*cap)
    return r
async def get_data1(param_array,height,width,image):
    point1 = await create_point(param_array[0],param_array[1],height,width)
    point2 = await create_point(param_array[2],param_array[3],height,width)
    point3 = await create_point(param_array[4],param_array[5],height,width)
    r =  await create_number(param_array[6],cap=255)
    g = await create_number(param_array[7],cap=255)
    b = await create_number(param_array[8],cap=255)
    alpha = await create_number(param_array[9],cap=255)

    # await point1
    # await point2
    # await point3 
    # await r
    # await g
    # await b
    # await alpha
    # print(point1)
    # print(point2)
    # print(point3)
    # print(r)
    # print(g)
    # print(b)
    # print(alpha)
    points= [point1,point2,point3]
    
    return points,r,g,b,alpha
async def render(params,height,width):
    image = Image.new('RGB',(width,height))
    drw = ImageDraw.Draw(image,'RGBA')
    k=[]
    for i in range(len(params)):
        k.append(get_data1(params[i],height,width,image))
    all_data = await asyncio.gather(*k)
    
    for points,r,g,b,alpha in all_data:
        # alpha = 1.0/params.shape[0]
        # print(points.dtype)
        # print(type(alpha))
        
        drw.polygon(points, (r,g,b,alpha))
    del drw
    return np.array(image)
def get_data(param_array,height,width):
    point1 = (int(param_array[0]*height),int(param_array[1]*width))
    point2 = (int(param_array[2]*height),int(param_array[3]*width))
    point3 = (int(param_array[4]*height),int(param_array[5]*width))
    r =  int(param_array[6]*255)
    g = int(param_array[7]*255)
    b = int(param_array[8]*255)
    alpha = param_array[9]
    return np.array([point1,point2,point3]),r,g,b,alpha
def render1(params,height,width):
    image = np.ones((height, width, 3), np.uint8) * 255
    for i in range(params.shape[0]):
        points,r,g,b,alpha= get_data(params[i],height,width)
        alpha = 1.0/params.shape[0]
        # print(r,g,b,alpha)
        # print("points",points,file=f)
        cv2.drawContours(image,[points],0,(r,g,b,alpha),-1)
    return image.astype('float32')
if __name__=="__main__":
    import numpy as np
    import cv2
    import time
    from util import *
    import multiprocessing
    import torch
    import pickle
    import asyncio
    with open('checkpoint','rb') as f:
        means,std,velocity1,velocity2 = pickle.load(f)

    # means = 
    x = [torch.normal(mean = means,std = std) for i in range(10)]
    
    # cv2.imshow("image",image)
    # cv2.waitKey()
    start = time.time()
    # p = multiprocessing.Pool(processes=4)
    arr = []
    results = []
    # print(x[0])
    for i in range(len(x)):
    #     arr.append(p.apply_async(render,([x[i],2000,2000])))

    
    # for i in range(len(arr)):
    #     arr[i].wait()
        # results.append(arr[i].get())
        t = asyncio.run(render(x[i],1453,2048))
        results.append(t)
        # print(i)
        # for param in x[i]:
        #     triangle = asyncio.run(get_data1(param,1453,2048,None))
        #     print(triangle)
    # p.close()
    # p.join()

    
    print(time.time()-start)
    Image.fromarray(results[0]).save('_t3.png','PNG')
    
