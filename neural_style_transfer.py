import torch
import numpy as np
import os
import argparse
import utils.utils as utils
from torch.optim import Adam, LBFGS
from torch.autograd import Variable
from typing import Tuple, List, Callable


class Config:
    def __init__(self,
                 content_images_dir: str,
                 content_img_name: str,
                 style_images_dir: str,
                 style_img_name: str,
                 output_img_dir: str,
                 height: int,
                 model: str,
                 init_method: str,
                 optimizer: str,
                 content_weight: float,
                 style_weight: float,
                 tv_weight: float,
                 saving_freq: int,
                 img_format: Tuple[int, str],
                 total_iterations: int,
                 learning_rate: float):
        self.content_images_dir = content_images_dir
        self.content_img_name = content_img_name
        self.style_images_dir = style_images_dir
        self.style_img_name = style_img_name
        self.output_img_dir = output_img_dir
        self.height = height
        self.model = model
        self.init_method = init_method
        self.optimizer = optimizer
        self.content_weight = content_weight
        self.style_weight = style_weight
        self.tv_weight = tv_weight
        self.saving_freq = saving_freq
        self.img_format = img_format
        self.total_iterations = total_iterations
        self.learning_rate = learning_rate


class NeuralStyleTransfer:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.neural_net, self.content_index, self.style_indices = self._prepare_model()
        self.task_ID: str = None

    def set_task_ID(self, task_ID: str) -> None:
        self.task_ID = task_ID

    def _prepare_model(self) -> Tuple[torch.nn.Module, List[int], List[int]]:
        neural_net, content_index, style_indices = utils.prepare_model(self.config.model, self.device)
        print(f'Using {self.config.model} in the optimization procedure.')
        return neural_net, content_index, style_indices

    def build_loss(self, optimizing_img: torch.Tensor, target_representations: List[torch.Tensor]) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        target_content_representation = target_representations[0]
        target_style_representation = target_representations[1]

        current_set_of_feature_maps = self.neural_net(optimizing_img)

        current_content_representation = current_set_of_feature_maps[self.content_index[0]].squeeze(axis=0)
        content_loss = torch.nn.MSELoss(reduction='mean')(target_content_representation, current_content_representation)

        style_loss = 0.0
        current_style_representation = [utils.gram_matrix(x) for cnt, x in enumerate(current_set_of_feature_maps) if
                                        cnt in self.style_indices[0]]
        for gram_gt, gram_hat in zip(target_style_representation, current_style_representation):
            style_loss += torch.nn.MSELoss(reduction='sum')(gram_gt[0], gram_hat[0])
        style_loss /= len(target_style_representation)

        tv_loss = utils.total_variation(optimizing_img)

        total_loss = self.config.content_weight * content_loss + self.config.style_weight * style_loss + \
                     self.config.tv_weight * tv_loss

        return total_loss, content_loss, style_loss, tv_loss

    def make_tuning_step(self, optimizer: torch.optim.Optimizer, target_representations: List[torch.Tensor]) -> Callable[[torch.Tensor], Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]]:
        def tuning_step(optimizing_img: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
            total_loss, content_loss, style_loss, tv_loss = self.build_loss(optimizing_img, target_representations)
            total_loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            return total_loss, content_loss, style_loss, tv_loss

        return tuning_step

    def _prepare_init_image(self, content_img: torch.Tensor, style_img: torch.Tensor) -> Variable:
        if self.config.init_method == 'random':
            gaussian_noise_img = np.random.normal(loc=0, scale=90., size=content_img.shape).astype(np.float32)
            init_img = torch.from_numpy(gaussian_noise_img).float().to(self.device)
        elif self.config.init_method == 'content':
            init_img = content_img
        else:
            style_img_resized = utils.prepare_img(style_img, np.asarray(content_img.shape[2:]), self.device)
            init_img = style_img_resized

        return Variable(init_img, requires_grad=True)

    def _prepare_target_representations(self, content_img: torch.Tensor, style_img: torch.Tensor) -> List[torch.Tensor]:
        content_img_set_of_feature_maps = self.neural_net(content_img)
        style_img_set_of_feature_maps = self.neural_net(style_img)

        target_content_representation = content_img_set_of_feature_maps[self.content_index[0]].squeeze(axis=0)
        target_style_representation = [utils.gram_matrix(x) for cnt, x in enumerate(style_img_set_of_feature_maps) if
                                       cnt in self.style_indices[0]]

        return [target_content_representation, target_style_representation]

    def optimize(self) -> str:
        content_img_path = os.path.join(self.config.content_images_dir, self.config.content_img_name)
        style_img_path = os.path.join(self.config.style_images_dir, self.config.style_img_name)

        out_dir_name = 'combined_' + os.path.split(content_img_path)[1].split('.')[0] + '_' + \
                       os.path.split(style_img_path)[1].split('.')[0]
        dump_path = os.path.join(self.config.output_img_dir, out_dir_name)
        os.makedirs(dump_path, exist_ok=True)

        content_img = utils.prepare_img(content_img_path, self.config.height, self.device)
        style_img = utils.prepare_img(style_img_path, self.config.height, self.device)

        optimizing_img = self._prepare_init_image(content_img, style_img)
        target_representations = self._prepare_target_representations(content_img, style_img)

        num_of_iterations = self.config.total_iterations if self.config.total_iterations else {
            "lbfgs": 1000,
            "adam": 3000,
        }[self.config.optimizer]

        if self.config.optimizer == 'adam':
            optimizer = Adam((optimizing_img,), lr=self.config.learning_rate)
            tuning_step = self.make_tuning_step(optimizer, target_representations)
            for cnt in range(num_of_iterations):
                total_loss, content_loss, style_loss, tv_loss = tuning_step(optimizing_img)
                with torch.no_grad():
                    print(
                        f'Adam | iteration: {cnt:03}, total loss={total_loss.item():12.4f}, content_loss={self.config.content_weight * content_loss.item():12.4f}, style loss={self.config.style_weight * style_loss.item():12.4f}, tv loss={self.config.tv_weight * tv_loss.item():12.4f}')
                    utils.save_and_maybe_display(optimizing_img, dump_path, self.config, cnt,
                                                 num_of_iterations, should_display=False)
        elif self.config.optimizer == 'lbfgs':
            optimizer = LBFGS((optimizing_img,), max_iter=num_of_iterations, line_search_fn='strong_wolfe')
            cnt = 0

            def closure() -> torch.Tensor:
                nonlocal cnt
                if torch.is_grad_enabled():
                    optimizer.zero_grad()
                total_loss, content_loss, style_loss, tv_loss = self.build_loss(optimizing_img, target_representations)
                if total_loss.requires_grad:
                    total_loss.backward()
                with torch.no_grad():
                    print(
                        f'L-BFGS | iteration: {cnt:03}, total loss={total_loss.item():12.4f}, content_loss={self.config.content_weight * content_loss.item():12.4f}, style loss={self.config.style_weight * style_loss.item():12.4f}, tv loss={self.config.tv_weight * tv_loss.item():12.4f}')
                    utils.save_and_maybe_display(optimizing_img, dump_path, self.config, cnt,
                                                 num_of_iterations, should_display=False)

                cnt += 1
                return total_loss

            optimizer.step(closure)

        return dump_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Neural Style Transfer')
    parser.add_argument('--content-image-path', type=str, default='./data/content/vader.png',
                        help='Path to content image')
    parser.add_argument('--style-image-path', type=str, default='./data/style/japan_1.jpg', help='Path to style image')
    parser.add_argument('--content-weight', type=float, default=5, help='Content loss weight')
    parser.add_argument('--style-weight', type=float, default=1e2, help='Style loss weight')
    parser.add_argument('--tv-weight', type=float, default=1e-3, help='Total variation loss weight')
    parser.add_argument('--optimizer', type=str, choices=['lbfgs', 'adam'], default='lbfgs', help='Optimizer choice')
    parser.add_argument('--model', type=str, choices=['vgg16', 'vgg19'], default='vgg19', help='Pre-trained model')
    parser.add_argument('--init-method', type=str, choices=['random', 'content', 'style'], default='content',
                        help='Initialization method')
    parser.add_argument('--total-iterations', type=int, default=100, help='Total number of optimization iterations')
    parser.add_argument('--learning-rate', type=float, default=1, help='Learning rate for Adam optimizer')
    parser.add_argument('--height', type=int, default=400, help='Height of the input images')
    parser.add_argument('--output-folder', type=str, default='output_image', help='Filename for the optimized output image')

    args = parser.parse_args()


    config = Config(
        content_images_dir=os.path.dirname(args.content_image_path),
        content_img_name=os.path.basename(args.content_image_path),
        style_images_dir=os.path.dirname(args.style_image_path),
        style_img_name=os.path.basename(args.style_image_path),
        output_img_dir=os.path.dirname(args.output_folder),
        height=args.height,
        model=args.model,
        init_method=args.init_method,
        optimizer=args.optimizer,
        content_weight=args.content_weight,
        style_weight=args.style_weight,
        tv_weight=args.tv_weight,
        saving_freq=100,
        img_format=(4, '.jpg'),
        total_iterations=args.total_iterations,
        learning_rate=args.learning_rate
    )

    nst = NeuralStyleTransfer(config)
    optimized_image_path = nst.optimize()
