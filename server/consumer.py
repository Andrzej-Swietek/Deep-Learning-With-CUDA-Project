import base64

from kafka import KafkaConsumer
import json
import os
import sys
import signal
import redis
import logging
from PIL import Image
from io import BytesIO

from kafka.errors import KafkaError

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from neural_style_transfer import NeuralStyleTransfer

stop_consumer = False

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Signal handler to gracefully shut down the consumer
def signal_handler(sig, frame):
    global stop_consumer
    print('\nShutting down gracefully...')
    consumer.close()
    print(f'[LOG]: KAFKA CONSUMER STOPPED')
    logger.info('KAFKA CONSUMER STOPPED')
    exit(0)


def decode_image(base64_string):
    # Remove prefix if present
    if base64_string.startswith('data:image/'):
        base64_string = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(image_data))

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

consumer = KafkaConsumer(
    'style_transfer',
    bootstrap_servers='kafka:29092',     # DOCKER
    # bootstrap_servers='0.0.0.0:9092', # LOCAL
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    max_partition_fetch_bytes=4097152  # Set to a larger value, e.g., 2 MB
)
redis_client = redis.Redis(host='redis', port=6379, db=0)

print(f'[LOG]: KAFKA CONSUMER STARTED')
logger.info('KAFKA CONSUMER STARTED')

try:
    for message in consumer:
        if stop_consumer:
            break

        task = message.value
        task_id = task['task_id']
        content_image_path = task['content_image_path']
        style_image_path = task['style_image_path']
        content_image_base64 = task['content_image']
        style_image_base64 = task['style_image']

        # Decode the images
        content_image = decode_image(content_image_base64)
        style_image = decode_image(style_image_base64)

        # Convert to RGB mode if needed (for pillow)
        if content_image.mode == 'RGBA':
            content_image = content_image.convert('RGB')
        if style_image.mode == 'RGBA':
            style_image = style_image.convert('RGB')

        content_image.save(content_image_path)
        style_image.save(style_image_path)

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
        nst.set_task_ID(task_id)

        output_path = f"../output/{task_id}"
        os.makedirs(output_path, exist_ok=True)
        result = nst.optimize()

        print(f"Task {task_id} completed. Output saved to {output_path}")
        logger.info(f"Task {task_id} completed. Output saved to {output_path}")

        # Update the status of the task in Redis
        redis_client.set(task_id, 'Finished')
except KafkaError as e:
    logger.info(f'KAFKA CONSUMER: \n {e} \n\n')

finally:
    consumer.close()
    print(f'[LOG]: KAFKA CONSUMER STOPPED')
    logger.info('KAFKA CONSUMER STOPPED')