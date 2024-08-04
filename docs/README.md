# Neural Style Transfer
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=git,python,pytorch,anaconda" />
  </a>
</p>
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=flask,kafka,svelte,tailwind" />
  </a>
</p>

## About
Neural Style Transfer is a deep learning technique that applies the style of one image to the content of another image. This project leverages popular frameworks and tools such as PyTorch for model implementation, Flask for backend API, Svelte for the frontend, Kafka for communication, and Redis for caching. The primary goal is to create a web service where users can perform neural style transfer on their images.


## Features

- <b>Web Interface:</b> Easy-to-use frontend for uploading images and applying style transfer.
- <b>Backend API:</b> Robust backend built with Flask to handle image processing requests.
- <b>Real-time Processing:</b> Utilizing Kafka for efficient communication and Redis for caching results.
- <b>Dockerized Services:</b> All components are containerized for easy deployment.

## Running Web Service

### Docker
To run the application using Docker, you can use the following command:
```shell
docker-compose up --build -d 
```

| Service    | Listening Port          |
|------------|-------------------------|
| Frontend   | http://localhost:5173/  |
| Backend    | http://localhost:5000/  |
| Consumer   | Communication via Kafka |
| Redis      | http://localhost:6379/  |
| Kafka      | http://localhost:9092/  |
| Zoo Keeper | http://localhost:2181/  |


## Usage Manual
### Web Service
![image](https://github.com/Andrzej-Swietek/Deep-Learning-With-CUDA-Project/blob/dev/docs/image1.png?raw=true)
1. Open browser @ `http://localhost:5173/`
2. Press `Start` button in navbar section

![image](https://github.com/Andrzej-Swietek/Deep-Learning-With-CUDA-Project/blob/dev/docs/image2.png?raw=true)

3. Either drag and Drop file from your computer or press button `Choose File`

    - Mind the file sizes: it's the best not to exceed `2MB` per image
    - Supported file formats: `.jpg` | `.png` ( webp not supported )
   
4. Once style transfer in completed two buttons shall be displayed in the header section.

   - a) Download     - Download last generated image ( default 1000 iteration )
   - b) Download Zip - Downloads all generated images as ZIP archive


#### CPU vs GPU
By default docker containers do not use GPU however `Consumer` container for better performance can be able to utilize GPU.


- **CPU**
   
  To use the CPU, you can modify the Dockerfile.consumer as follows:


```dockerfile
FROM python:3.9-slim

...
```
If choosing this option it is a good practice to ensure proper resources available: 
   * CPU with multimple threads
   * 16GB of RAM
   * Lot's of free time
   
___

- **GPU**

   To use the GPU, you can modify the Dockerfile as follows:


```dockerfile
# NVIDIA's PyTorch image as the base image
FROM nvcr.io/nvidia/pytorch:22.06-py3

...
```

Ensure that you have the necessary NVIDIA drivers and Docker support for GPU usage.

#### Structure:

```
+-------------------+      +-------------------+     +------------------------+
|                   |      |                   |     |                        |
|     Frontend      |      |      Backend      |     |     Tasks Queue        |
|     (Svelte)      | ---> |   (Flask/FastAPI) | --> |      (Kafka)           |
|                   |      |                   |     |                        |
+-------------------+      +-------------------+     +------------------------+
                                                                |       ^
                                                                v       |
+------------------------+     +---------------------+   +--------------------+
|                        |     |                     |   |                    |
|      File Storage      | <-- |     Data Base       |   |   Task Consumers   |
|    (AWS S3 / Local)    |     |  (PostgreSQL/Redis) |   |  (Python + Kafka)  |
|                        |     |                     |   |        NST         |
+------------------------+     +---------------------+   +--------------------+
                                                                |        ^
                                                                v        |
                                                        +-----------------------+
                                                        |  Monitorowanie        |
                                                        | (Prometheus + Grafana)|
                                                        +-----------------------+
```

### CLI
To use the CLI, run the following command:

```shell
python neural_style_transfer.py \
      --content_image_path <path_to_content_image> \
      --style_image_path <path_to_style_image> [options]
```

Example: 
```shell 
python3 neural_style_transfer.py \
      --content_image_path ./data/content/midjourney_2.png \
      --style_image_path ./data/style/japan_1.jpg
```


#### Options:

| Argument            | Type   | Default                          | Description                                  |
|---------------------|--------|----------------------------------|----------------------------------------------|
| --content_image_path| str    | ./data/content/star_wars_1.jpg   | Path to the content image                    |
| --style_image_path  | str    | ./data/style/japan.jpg           | Path to the style image                      |
| --content_weight    | float  | 1e5                              | Content loss weight                          |
| --style_weight      | float  | 3e4                              | Style loss weight                            |
| --tv_weight         | float  | 1e0                              | Total variation loss weight                  |
| --optimizer         | str    | lbfgs                            | Optimizer choice (lbfgs or adam)             |
| --model             | str    | vgg19                            | Pre-trained model (vgg16 or vgg19)           |
| --init_method       | str    | content                          | Initialization method (random, content, style)|
| --total_iterations  | int    | 20000                            | Total number of optimization iterations      |
| --learning_rate     | float  | 1.0                              | Learning rate for Adam optimizer             |
| --height            | int    | 400                              | Height of the input images                   |
| --output_file       | str    | output_image.jpg                 | Filename for the optimized output image      |

All images are saved in `./data/output` folder. Format:
`./data/output/combined_[content_image_name]_[style_image_name]`

## References
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [Flask Documentation](https://azcv.readthedocs.io/en/latest/)
- [Docker Documentation](https://docs.docker.com/)
- [Kafka Documentation](https://kafka.apache.org/documentation/)


## Neural Style Transfer: Detailed Explanation

Neural style transfer is a technique that merges the content of one image with the style of another by leveraging deep neural networks. The process involves extracting feature representations of both images using a pre-trained Convolutional Neural Network (CNN) and then optimizing a new image to match the content features of the content image and the style features of the style image. Here's a detailed explanation of how this process works:

1. **Initialization**
   The `NeuralStyleTransfer` class initializes with a configuration dictionary, which includes paths to images, model selection, weights for different loss components, and optimization parameters. The initialization method sets the computation device (GPU if available, otherwise CPU) and prepares the neural network model.
   ```python
      class NeuralStyleTransfer:
        def __init__(self, config):
           self.config = config
           self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
           self.neural_net, self.content_index, self.style_indices = self._prepare_model()
           self.task_ID = None
   ```
2. **Model Preparation**
   The _prepare_model method loads a pre-trained VGG16 or VGG19 model and identifies the layers to be used for content and style extraction. The utils.prepare_model function handles the specifics of loading the model and extracting relevant layers.
   ```python
   def _prepare_model(self):
        neural_net, content_index, style_indices = utils.prepare_model(self.config['model'], self.device)
        print(f'Using {self.config["model"]} in the optimization procedure.')
        return neural_net, content_index, style_indices
   ```
3. **Feature Extraction**


   **Content Extraction:** The content of an image is represented by the activations (feature maps) of a specific layer in the CNN when the image is passed through it. Typically, a deeper layer is chosen because it captures higher-level features.


   **Style Extraction:** The style of an image is represented by the correlations between the different feature maps at multiple layers, which can be captured using Gram matrices. The Gram matrix of a set of feature maps is the dot product of the feature maps with their transpose.

   ```python
   def _prepare_target_representations(self, content_img, style_img):
       content_img_set_of_feature_maps = self.neural_net(content_img)
       style_img_set_of_feature_maps = self.neural_net(style_img)
   
       target_content_representation = content_img_set_of_feature_maps[self.content_index[0]].squeeze(axis=0)
       target_style_representation = [utils.gram_matrix(x) for cnt, x in enumerate(style_img_set_of_feature_maps) if cnt in self.style_indices[0]]
   
       return [target_content_representation, target_style_representation]
   ```
4. **Loss Functions**
   The total loss is a combination of three components:
   - **Content Loss:** Measures how much the content of the generated image differs from the content image. It is the mean squared error between the feature maps of the content image and the generated image.
   - **Style Loss:** Measures how much the style of the generated image differs from the style image. It is the mean squared error between the Gram matrices of the style image and the generated image.
   - **Total Variation (TV) Loss:** Encourages smoothness in the generated image. It is the sum of the absolute differences between neighboring pixel values.
```python
def build_loss(self, optimizing_img, target_representations):
    target_content_representation = target_representations[0]
    target_style_representation = target_representations[1]

    current_set_of_feature_maps = self.neural_net(optimizing_img)

    current_content_representation = current_set_of_feature_maps[self.content_index[0]].squeeze(axis=0)
    content_loss = torch.nn.MSELoss(reduction='mean')(target_content_representation, current_content_representation)

    style_loss = 0.0
    current_style_representation = [utils.gram_matrix(x) for cnt, x in enumerate(current_set_of_feature_maps) if cnt in self.style_indices[0]]
    for gram_gt, gram_hat in zip(target_style_representation, current_style_representation):
        style_loss += torch.nn.MSELoss(reduction='sum')(gram_gt[0], gram_hat[0])
    style_loss /= len(target_style_representation)

    tv_loss = utils.total_variation(optimizing_img)

    total_loss = self.config['content_weight'] * content_loss + self.config['style_weight'] * style_loss + self.config['tv_weight'] * tv_loss

    return total_loss, content_loss, style_loss, tv_loss
```

5. **Image Initialization**
   The initial image can be set to:
   - Random noise
   - The content image
   - The style image
   
   This initial image is the starting point for the optimization process.
   
```python
def _prepare_init_image(self, content_img, style_img):
    if self.config['init_method'] == 'random':
        gaussian_noise_img = np.random.normal(loc=0, scale=90., size=content_img.shape).astype(np.float32)
        init_img = torch.from_numpy(gaussian_noise_img).float().to(self.device)
    elif self.config['init_method'] == 'content':
        init_img = content_img
    else:
        style_img_resized = utils.prepare_img(style_img, np.asarray(content_img.shape[2:]), self.device)
        init_img = style_img_resized

    return Variable(init_img, requires_grad=True)
```

6. **Optimization**
7. **Execution**
8. **Summary**
   The neural style transfer process works by optimizing an initial image to minimize a combination of content loss, style loss, and total variation loss. The content loss ensures that the generated image retains the content of the original content image, while the style loss ensures that it captures the style of the style image. The total variation loss helps in smoothing the generated image. By iteratively updating the image based on the computed losses, the algorithm produces an image that combines the content and style in a visually appealing manner.
