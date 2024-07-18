from kafka import KafkaConsumer
import json
import os
from neural_style_transfer import NeuralStyleTransfer
import utils

consumer = KafkaConsumer(
    'style_transfer',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    task = message.value
    task_id = task['task_id']
    content_image_path = task['content_image_path']
    style_image_path = task['style_image_path']

    config = {
        'content_images_dir': os.path.dirname(content_image_path),
        'content_img_name': os.path.basename(content_image_path),
        'style_images_dir': os.path.dirname(style_image_path),
        'style_img_name': os.path.basename(style_image_path),
        'output_img_dir': '/output',
        'height': 400,
        'model': 'vgg19',
        'init_method': 'content',
        'optimizer': 'lbfgs',
        'content_weight': 1e5,
        'style_weight': 3e4,
        'tv_weight': 1e0,
        'saving_freq': 100,
        'img_format': (4, '.jpg')
    }

    nst = NeuralStyleTransfer(config)
    output_path = f"/output/{task_id}"
    os.makedirs(output_path, exist_ok=True)
    result = nst.optimize()

    # You can also update the status of the task in the database here
    # and notify the frontend when the processing is done.
