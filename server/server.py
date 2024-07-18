from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
import json
import os
import uuid
import redis

app = Flask(__name__)


class Server:
    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)
        self.producer = KafkaProducer(bootstrap_servers='kafka:9092',
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    @app.route('/api/style_transfer', methods=['POST'])
    def style_transfer(self):
        content_image = request.files['content_image']
        style_image = request.files['style_image']
        task_id = str(uuid.uuid4())

        # Save images locally for processing by the consumer
        content_image_path = f"/tmp/{task_id}_content.jpg"
        style_image_path = f"/tmp/{task_id}_style.jpg"
        content_image.save(content_image_path)
        style_image.save(style_image_path)

        # Send task to Kafka
        task = {
            'task_id': task_id,
            'content_image_path': content_image_path,
            'style_image_path': style_image_path,
        }
        self.producer.send('style_transfer', task)

        # Save initial task status to Redis
        self.redis_client.set(task_id, 'Processing')

        return jsonify({'task_id': task_id}), 202

    @app.route('/api/task_status/<task_id>', methods=['GET'])
    def task_status(self, task_id):
        status = self.redis_client.get(task_id)
        if status is None:
            return jsonify({'task_id': task_id, 'status': 'Unknown'}), 404
        return jsonify({'task_id': task_id, 'status': status.decode('utf-8')})

    def run(self, port):
        app.run(host='0.0.0.0', port=port, debug=True)
