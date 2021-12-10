import numpy as np
import torch
async def fitness(img1,img2):
    # img1 = torch.tensor(img1)
    # img2 = torch.tensor(img2)
    r = ((img1-img2)**2).mean()
    return r