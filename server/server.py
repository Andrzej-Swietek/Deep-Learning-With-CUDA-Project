import base64
import logging
import shutil

from flask import Flask, request, jsonify, make_response, send_file
from kafka import KafkaProducer
import json
import os
import uuid
import redis
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # 16MB
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Redis and Kafka clients
redis_client = redis.Redis(host='redis', port=6379, db=0)
producer = KafkaProducer(
    bootstrap_servers='kafka:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    max_request_size=4097152
)


def encode_image(image):
    file_content = image.read()
    return base64.b64encode(file_content).decode('utf-8')


@app.route('/api/style_transfer', methods=['POST'])
@cross_origin()
def style_transfer():
    content_image = request.files['content_image']
    style_image = request.files['style_image']

    logger.info('\ncontent_image:\n')
    logger.info('\n{}:\n'.format(str(content_image)))

    if not content_image or not style_image:
        return jsonify({'error': 'Both content_image and style_image are required'}), 400

    task_id = str(uuid.uuid4())

    # Save images locally for processing by the consumer
    content_image_path = f"./tmp/{task_id}_content.jpg"
    style_image_path = f"./tmp/{task_id}_style.jpg"

    # Ensure the tmp directory exists
    os.makedirs(os.path.dirname(content_image_path), exist_ok=True)

    # content_image.save(content_image_path)
    # style_image.save(style_image_path)

    try:
        # Encode images to base64
        encoded_content_image = encode_image(content_image)
        encoded_style_image = encode_image(style_image)

        task = {
            'task_id': task_id,
            'content_image_path': content_image_path,
            'style_image_path': style_image_path,
            'content_image': encoded_content_image,
            'style_image': encoded_style_image,
        }

        # Send task to Kafka
        producer.send('style_transfer', task)

        # Save initial task status to Redis
        redis_client.set(task_id, 'Processing')

        return jsonify({'task_id': task_id}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/task_status/<task_id>', methods=['GET'])
@cross_origin()
def task_status(task_id):
    status = redis_client.get(task_id)
    if status is None:
        return jsonify({'task_id': task_id, 'status': 'Unknown'}), 404
    return jsonify({'task_id': task_id, 'status': status.decode('utf-8')})


@app.route('/api/download/<task_id>', methods=['GET'])
@cross_origin()
def download(task_id):
    task = redis_client.get(task_id)
    task_status = task.decode('utf-8')
    if task is None:
        return jsonify({'task_id': task_id, 'status': 'Unknown'}), 404

    if task_status in ['Finished', 'Completed']:
        output_path = f"../output/{task_id}/1000.jpg"
        if os.path.exists(output_path):
            return send_file_with_attachment(output_path, 'result.jpg')
        else:
            return jsonify({
                'task_id': task_id,
                'status': 'Output file not found'
            }), 404
    else:
        return jsonify({'task_id': task_id, 'status': f'In Progress: [{task_status}]'}), 404


@app.route('/api/download-all/<task_id>', methods=['GET'])
@cross_origin()
def download_zip(task_id):
    task = redis_client.get(task_id)
    if task is None:
        return jsonify({'task_id': task_id, 'status': 'Unknown'}), 404

    task_status = task.decode('utf-8')
    if task_status not in ['Finished', 'Completed']:
        return jsonify({'task_id': task_id, 'status': f'In Progress: [{task_status}]'}), 202

    # Path to the folder to be zipped
    folder_path = f"../output/{task_id}"
    zip_path = f"../output/{task_id}.zip"

    # Create a zip file
    shutil.make_archive(zip_path[:-4], 'zip', folder_path)

    # Send the zip file
    try:
        return send_file_with_attachment(zip_path, f'{task_id}.zip')
    finally:
        # Remove the zip file after sending it
        os.remove(zip_path)


def send_file_with_attachment(file_path, filename):
    response = make_response(send_file(file_path))
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
