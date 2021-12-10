import torch
class ClipUp:
    def __init__(self,velocity=0,v_max = 0.1,momentum = 0.9,step_size = None):
        self.velocity = velocity
        self.v_max = v_max
        self.momentum = momentum
        if step_size is None:
            self.step_size = v_max/2
        else:
            self.step_size = step_size
    def __call__(self,param_tensor):
        _v = self.momentum*self.velocity+self.step_size*(param_tensor/torch.norm(param_tensor,2))
        dist = torch.norm(_v,2)
        if dist>self.v_max:
            new_v = self.v_max*(_v/dist)
        else:
            new_v = _v
        self.velocity = new_v
        return new_v

