from flask import Flask, request, jsonify
import json
import os
import uuid

from server import Server

if __name__ == '__main__':
    server_instance = Server()
    server_instance.run()
