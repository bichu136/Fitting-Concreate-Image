from render import *
import numpy as np
import cv2
import time
from util import *
import multiprocessing
import asyncio
from fitness import *
import torch
import pickle
from clipup_op import *
from PIL import Image
# init means and std
NUMBER_OF_TRIANGLE = 100
def random_tensor(tensor):
    idx = torch.randperm(NUMBER_OF_TRIANGLE)
    tensor = tensor[idx]
    return tensor
try :
    print("load from checkpoint")
    f = open('checkpoint','rb')
    means,std,velocity_means,velocity_std = pickle.load(f)
    f.close()
except:
    print("init new params")
    means = torch.zeros((NUMBER_OF_TRIANGLE,10)) +0.5
    std = torch.zeros((NUMBER_OF_TRIANGLE,10)) +0.5
    velocity_means = 0
    velocity_std = 0
# learning_rate = 0.0000000001

async def generate_pop(population,mean,std):
    # print(std)
    for j in range(population):
        yield torch.normal(mean = mean,std = std).numpy()


def get_fitness_from_generator(population_generator):
    for i in population_generator:
        yield fitness(render1(i,gt.shape[0],gt.shape[1]),gt)
async def get_fitness(population,gt,i):
    # j = 0
    # for i in population:
        # j+=1
        # print(j/512,end="\r")
        x = await render(population[i],gt.shape[0],gt.shape[1])
        r = await fitness(x,gt)
        return r
async def main():
    global means
    global std
    global velocity_means
    global velocity_std
    gt = Image.open('gt.jpg')
    gt = np.array(gt)
    optimizer_means = ClipUp(velocity=velocity_means)
    optimizer_std = ClipUp(velocity=velocity_std)
    for gen in range(10000000):
        print(gen)
        start =time.time()

        population_generator = generate_pop(512,means,std)
        population = [i async for i in population_generator]

        
        # cv2.imshow("image",image)
        # cv2.waitKey()
        arr = []
        
        q = []
        for i in range(len(population)):
            q.append(get_fitness(population,gt,i))
        
        results = await asyncio.gather(*q)
        print(time.time()-start)
        # results = [-i for i in results]
        
        r = results
        # r = []
        # j = 0
        # for i in results:
        #     print(j/512,end="\r")
        #     r.append(-i)
        #     j+=1

        # do the gradient thing

        population = torch.tensor(population)
        T = population - means
        S = (T**2-std**2)/std
        r = (-torch.tensor(r).reshape(len(r),1))/(255*255)
        T = T.reshape(T.shape[0],T.shape[1]*T.shape[2]).transpose(0,1)
        
        d_means = torch.matmul(T.float(),r.float())
        
        d_means = d_means.reshape(NUMBER_OF_TRIANGLE,10)

        S = S.reshape(S.shape[0],S.shape[1]*S.shape[2]).transpose(0,1)
        d_std = torch.matmul(S.float(),r.float())
        d_std = d_std.reshape(NUMBER_OF_TRIANGLE,10)
        # update gradient for randomizer
        means = means + optimizer_means(d_means)
        new_std = std+optimizer_std(d_std)
        threshold = torch.nn.Threshold(-0.5,-0.5)
        new_std = -threshold(-new_std)
        # print(c_std)
        # threshold = torch.nn.Threshold(0,1)
        # c_std = threshold(0-c_std)
        # # print(c_std)
        # std = new_std*c_std+std*(1-c_std)
        std = new_std

        with open("result.txt",'a') as result_file:
            print(r.mean(),file=result_file)
        
        with open("mean_std.txt","w") as mean_std_file:
            print("mean = ",means.mean(),file = mean_std_file)
            print("std = ",std.mean(),file = mean_std_file)
        
            print("velocity of mean = ",optimizer_means.velocity.mean(),file = mean_std_file)
            print("velocity of std = ",optimizer_std.velocity.mean(),file = mean_std_file)
        x= optimizer_std.velocity.mean()
        print(x<1.00e-20 and x>-1.00e-20)
        if (x<1.00e-20 and x>-1.00e-20):
            break
        
    #repeat

        checkpoint = (means,std,optimizer_means.velocity,optimizer_std.velocity)
        with open('checkpoint','wb') as f:
            pickle.dump(checkpoint,f)

start = time.time()
asyncio.run(main())
print(time.time()-start)
