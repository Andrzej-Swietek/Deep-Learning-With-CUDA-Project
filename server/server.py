from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
import json
import os
import uuid
import redis

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)
        self.producer = KafkaProducer(bootstrap_servers='kafka:9092',
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        # Register routes
        self.app.add_url_rule('/api/style_transfer', view_func=self.style_transfer, methods=['POST'])
        self.app.add_url_rule('/api/task_status/<task_id>', view_func=self.task_status, methods=['GET'])

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

    def task_status(self, task_id):
        status = self.redis_client.get(task_id)
        if status is None:
            return jsonify({'task_id': task_id, 'status': 'Unknown'}), 404
        return jsonify({'task_id': task_id, 'status': status.decode('utf-8')})

    def run(self, port=5000):
        self.app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    server_instance = Server()
    server_instance.run()