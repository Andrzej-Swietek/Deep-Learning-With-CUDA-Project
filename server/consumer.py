from kafka import KafkaConsumer
import json
import os
import sys
import signal

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from neural_style_transfer import NeuralStyleTransfer

stop_consumer = False


# Signal handler to gracefully shut down the consumer
def signal_handler(sig, frame):
    global stop_consumer
    print('\nShutting down gracefully...')
    consumer.close()
    print(f'[LOG]: KAFKA CONSUMER STOPPED')
    exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

consumer = KafkaConsumer(
    'style_transfer',
    bootstrap_servers='kafka:9092',     # DOCKER
    # bootstrap_servers='0.0.0.0:9092', # LOCAL
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print(f'[LOG]: KAFKA CONSUMER STARTED')

try:
    for message in consumer:
        if stop_consumer:
            break

        task = message.value
        task_id = task['task_id']
        content_image_path = task['content_image_path']
        style_image_path = task['style_image_path']

        print(f'[LOG]: Task {task_id} | {content_image_path}')

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

        print(f"Task {task_id} completed. Output saved to {output_path}")

        # You can also update the status of the task in the database here
        # and notify the frontend when the processing is done.

finally:
    consumer.close()
    print(f'[LOG]: KAFKA CONSUMER STOPPED')