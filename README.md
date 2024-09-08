# Neural Style Transfer with Deep Learning

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=git,python,pytorch,anaconda" />
  </a>
</p>
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=flask,kafka,svelte" />
  </a>
</p>

## Authors

| Name              | GitHub Profile                                |
|-------------------|-----------------------------------------------|
| Andrzej Świętek   | [GitHub Profile](https://github.com/Andrzej-Swietek)   |
| Krzysztof Konieczny| [GitHub Profile](https://github.com/KrzysztofProgramming)|
| Jan Kwiatkowski   | [GitHub Profile](https://github.com/ZEN1X)   |

## About the Project

This project implements Neural Style Transfer (NST) using deep learning techniques and CUDA acceleration. The goal is to blend two images: one content image and one style image, to produce an image that maintains the content of the first image while adopting the artistic style of the second.

### Key Features

- **Deep Learning Framework**: Utilizes PyTorch for building and training neural networks.
- **CUDA Acceleration**: Leverages CUDA for faster computation and training on NVIDIA GPUs.
- **Flexible Style Transfer**: Supports various style transfer algorithms and parameter configurations.
- **Web Interface**: Includes a Flask-based web interface for easy experimentation with different images and styles.

### Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Andrzej-Swietek/Deep-Learning-With-CUDA-Project/
   cd Deep-Learning-With-CUDA-Project
   ```
2. **Launching app manual**
   
Follow this link for detailed description on how to start up the application using:
- Docker [link](https://github.com/Andrzej-Swietek/Deep-Learning-With-CUDA-Project/tree/main/docs#docker)
- CLI [link](https://github.com/Andrzej-Swietek/Deep-Learning-With-CUDA-Project/tree/main/docs#cli)
- General Information: [link](https://github.com/Andrzej-Swietek/Deep-Learning-With-CUDA-Project/tree/main/docs)

### Technical Documentation

<p align="center">
  <a href="https://github.com/Andrzej-Swietek/Deep-Learning-With-CUDA-Project/tree/main/docs">
     Tech Documentation 
  </a>
  &nbsp;
  <a href="https://github.com/Andrzej-Swietek/Deep-Learning-With-CUDA-Project/tree/main/docs/project_documentation.pdf">
     Descriptive Project Documentation 
  </a>
</p>


## Background

Neural Style Transfer (NST) is a technique in deep learning that allows us to combine the content of one image with the style of another. It leverages convolutional neural networks (CNNs) to achieve this artistic effect by separating and recombining the content and style representations of images.

### How It Works

1. **Feature Extraction**: Neural networks, particularly CNNs, are used to extract features from both the content image and the style image. These features capture different aspects of the images, such as textures, colors, and shapes.

2. **Loss Functions**: NST uses specific loss functions to measure the difference between the generated image and the content/style images. The content loss ensures that the generated image retains the content of the content image, while the style loss ensures that the generated image reflects the style of the style image.

3. **Optimization**: The generated image is iteratively updated to minimize the combined loss functions using optimization algorithms. This process blends the content and style images into the final output.

### Applications

- **Artistic Rendering**: NST is often used to create artistic versions of photos by applying the styles of famous artists or artwork.
- **Augmented Reality**: It can be used in AR applications to apply stylistic effects in real-time.
- **Design and Media**: Useful for graphic design and media content creation, allowing designers to apply unique styles to visual content.

### Key Components

- **Content Loss**: Measures the difference in content between the generated image and the content image.
- **Style Loss**: Measures the difference in style between the generated image and the style image.
- **Optimization Algorithm**: Adjusts the generated image to minimize the combined loss, often using techniques like gradient descent.

This project builds on the foundational principles of NST and leverages modern deep learning frameworks to provide a powerful tool for artistic image manipulation.
   
### Project Folder Structure
- **`data/`**: Contains input images and other necessary data for style transfer.
- **`data/output/`**: Stores the results of the style transfer process.
- **`docker-compose.yml`**: Configuration file for Docker Compose to manage multi-container Docker applications.
- **`docs/`**: Documentation and additional resources related to the project.
- **`frontend/`**: Frontend code and assets (Svelte).
- **`http/`**: HTTP server configurations and related files.
- **`models/`**: Directory for model checkpoints and configurations.
- **`neural_style_transfer.py`**: Main script for performing neural style transfer.
- **`notebooks/`**: Jupyter notebooks for experiments and analysis.
- **`server/`**: Backend server code (FLask API and worker/consumer).
- **`tmp/`**: Temporary files and directories for docker.
- **`utils/`**: Utility functions and helper modules.
- **`README.md`**: Project overview and instructions.
- **`'Team 1 - Style_Transfer_with_Deep_Learning.pdf'`**: Project prospect

