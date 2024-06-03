import torch
from torch.optim import Adam, LBFGS
from torch.autograd import Variable
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description='Neural Style Transfer',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

if __name__ == "__main__":
    if torch.cuda.is_available():
        print('=> Our gpu type and uploaded driver')
        os.system("nvidia-smi --query-gpu=gpu_name,driver_version --format=csv")
    else:
        print('==> There is no CUDA capable GPU device here!')
