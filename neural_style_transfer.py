import torch
from torch.optim import Adam, LBFGS
from torch.autograd import Variable
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description='Neural Style Transfer',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--content_image_path', type=str, default='./images/content/', help='Path to content image')
parser.add_argument('--style_image_path', type=str, default='./images/style/', help='Style image path')
parser.add_argument("--model", type=str, choices=['vgg11', 'vgg13', 'vgg16', 'vgg19', 'resnet'], default='vgg16',
                    help="Choose a pre-trained model")
parser.add_argument('--content_weight', default=1e5, help='Content loss weight')
parser.add_argument('--style_weight', default=3e5, help='Style loss weight')
parser.add_argument('--total_iterations', default=20000, type=int, help='Total number of iterations')
parser.add_argument('--batch_size', default=64, type=int, help='Batch size')
parser.add_argument('--learning_rate', default=1e-3, type=float, help='Learning rate')
parser.add_argument('--optimizer', type=str, choices=['adam', 'lbfgs'], help='Total number of iterations')

if __name__ == "__main__":
    if torch.cuda.is_available():
        print('=> Our gpu type and uploaded driver')
        os.system("nvidia-smi --query-gpu=gpu_name,driver_version --format=csv")
    else:
        print('==> There is no CUDA capable GPU device here!')
