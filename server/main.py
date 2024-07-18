from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
import json
import os
import uuid

from server.server import Server

if __name__ == '__main__':
    server = Server()
