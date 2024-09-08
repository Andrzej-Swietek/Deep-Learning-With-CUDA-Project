import os
from numbers import Number
from typing import Optional, Tuple, Union, List

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import Tensor
from torchvision import transforms

from models.vgg11 import Vgg11
from models.vgg13 import Vgg13
from models.vgg16 import Vgg16
from models.vgg19 import Vgg19
from neural_style_transfer import Config

IMAGENET_MEAN_255 = [123.675, 116.28, 103.53]
IMAGENET_STD_NEUTRAL = [1, 1, 1]

def load_image(img_path: str, target_shape: Optional[Union[int, Tuple[int, int]]] = None) -> np.ndarray:
    if not os.path.exists(img_path):
        raise Exception(f'Path does not exist: {img_path}')
    img = cv.imread(img_path)[:, :, ::-1]  # [:, :, ::-1] converts BGR (opencv format...) into RGB

    if target_shape is not None:  # resize section
        if isinstance(target_shape, int) and target_shape != -1:  # scalar -> implicitly setting the height
            current_height, current_width = img.shape[:2]
            new_height = target_shape
            new_width = int(current_width * (new_height / current_height))
            img = cv.resize(img, (new_width, new_height), interpolation=cv.INTER_CUBIC)
        else:  # set both dimensions to target shape
            img = cv.resize(img, (target_shape[1], target_shape[0]), interpolation=cv.INTER_CUBIC)

    img = img.astype(np.float32)  # convert from uint8 to float32
    img /= 255.0  # get to [0, 1] range
    return img


def prepare_img(img_path: str, target_shape: Union[int, Tuple[int, int]], device: torch.device) -> Tensor:
    img = load_image(img_path, target_shape=target_shape)

    # normalize using ImageNet's mean
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255)),
        transforms.Normalize(mean=IMAGENET_MEAN_255, std=IMAGENET_STD_NEUTRAL)
    ])

    img_tensor = transform(img).to(device).unsqueeze(0)

    return img_tensor


def save_image(img: np.ndarray, img_path: str) -> None:
    if len(img.shape) == 2:
        img = np.stack((img,) * 3, axis=-1)
    cv.imwrite(img_path, img[:, :, ::-1])  # [:, :, ::-1] converts RGB into BGR (opencv format...)


def generate_out_img_name(config: Config) -> str:
    prefix = os.path.basename(config.content_img_name).split('.')[0] + '_' + \
             os.path.basename(config.style_img_name).split('.')[0]
    # called from the reconstruction script
    if hasattr(config, 'reconstruct_script'):
        suffix = f'_o_{config.optimizer}_h_{str(config.height)}_m_{config.model}{config.img_format[1]}'
    else:
        suffix = f'_o_{config.optimizer}_i_{config.init_method}_h_{str(config.height)}_m_{config.model}_cw_{config.content_weight}_sw_{config.style_weight}_tv_{config.tv_weight}{config.img_format[1]}'
    return prefix + suffix


def save_and_maybe_display(optimizing_img: Tensor, dump_path: str, config: Config, img_id: int, num_of_iterations: Number, should_display: bool = False) -> None:
    saving_freq = config.saving_freq
    out_img = optimizing_img.squeeze(axis=0).to('cpu').detach().numpy()
    out_img = np.moveaxis(out_img, 0, 2)  # swap channel from 1st to 3rd position: ch, _, _ -> _, _, chr

    # for saving_freq == -1 save only the final result (otherwise save with frequency saving_freq and save the last pic)
    if img_id == num_of_iterations - 1 or (saving_freq > 0 and img_id % saving_freq == 0):
        img_format = config.img_format
        out_img_name = str(img_id).zfill(int(img_format[0])) + img_format[1] if saving_freq != -1 else generate_out_img_name(config)
        dump_img = np.copy(out_img)
        dump_img += np.array(IMAGENET_MEAN_255).reshape((1, 1, 3))
        dump_img = np.clip(dump_img, 0, 255).astype('uint8')
        cv.imwrite(os.path.join(dump_path, out_img_name), dump_img[:, :, ::-1])

    if should_display:
        plt.imshow(np.uint8(get_uint8_range(out_img)))
        plt.show()


def get_uint8_range(x: np.ndarray) -> np.ndarray:
    if isinstance(x, np.ndarray):
        x -= np.min(x)
        x /= np.max(x)
        x *= 255
        return x
    else:
        raise ValueError(f'Expected numpy array got {type(x)}')


def prepare_model(model, device) -> Tuple[torch.nn.Module, Tuple[int, str], Tuple[List[int], List[str]]]:
    experimental = False
    if model == 'vgg19':
        model = Vgg19(requires_grad=False, show_progress=True)
    elif model == 'vgg16':
        model = Vgg16(requires_grad=False, show_progress=True)
    elif model == 'vgg13':
        model = Vgg13(requires_grad=False, show_progress=True)
    elif model == 'vgg11':
        model = Vgg11(requires_grad=False, show_progress=True)
    else:
        raise ValueError(f'{model} not supported.')

    content_feature_maps_index = model.content_feature_maps_index
    style_feature_maps_indices = model.style_feature_maps_indices
    layer_names = model.layer_names

    content_fms_index_name = (content_feature_maps_index, layer_names[content_feature_maps_index])
    style_fms_indices_names = (style_feature_maps_indices, layer_names)
    return model.to(device).eval(), content_fms_index_name, style_fms_indices_names


def gram_matrix(x: Tensor, should_normalize: bool = True) -> Tensor:
    (b, ch, h, w) = x.size()
    features = x.view(b, ch, w * h)
    features_t = features.transpose(1, 2)
    gram = features.bmm(features_t)
    if should_normalize:
        gram /= ch * h * w
    return gram


def total_variation(y: Tensor) -> Tensor:
    return torch.sum(torch.abs(y[:, :, :, :-1] - y[:, :, :, 1:])) + \
           torch.sum(torch.abs(y[:, :, :-1, :] - y[:, :, 1:, :]))
