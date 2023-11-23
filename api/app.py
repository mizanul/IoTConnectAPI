"""
This module provides a Flask application for retrieving CPU, memory, 
and Docker container statistics.

It includes a simple authentication mechanism using 
Bearer tokens in the Authorization header.
"""
import os
import logging
from functools import wraps
import psutil
import docker
import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

logger = logging.getLogger(__name__)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] \
                                 [%(levelname)-5.5s]  %(message)s")
logger.setLevel(logging.DEBUG)
LOG_PATH="."
FILE_NAME="app"
FILE_HANDLER = logging.FileHandler(f"{LOG_PATH}/{FILE_NAME}.log")
FILE_HANDLER.setFormatter(logFormatter)
logger.addHandler(FILE_HANDLER)

# Get the secret key from the environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')

# Define the name of the authorization header
HEADER_NAME = 'Authorization'

def verify_request_header():
    """
    This is a decorator to check Bearer tokens in the Authorization header.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Get the Authorization header value
                auth_header = request.headers.get(HEADER_NAME)

                # Extract the key from the Authorization header
                if auth_header and auth_header.startswith('Bearer '):
                    api_key = auth_header.split(' ')[1]
                    logger.debug("api_key..... %s", api_key)
                    logger.debug("SECRET_KEY..... %s", SECRET_KEY)

                    # Verify the API key
                    if api_key == SECRET_KEY:
                        # Execute the original function
                        return func(*args, **kwargs)
                    return jsonify({'message': 'token is invalid'})
                # Return an error response if the Authorization header is missing or invalid
                return jsonify({'message': 'Authorization header is missing or invalid'})
            except IndexError as outer_exception:
                # Log the error
                logger.error("An error occurred: %s", str(outer_exception))
                # Handle the specific exception raised when the index is out of range
                return jsonify({'message': 'Invalid Authorization header format'})
        return wrapper
    return decorator

@app.route("/data/cpu")
@verify_request_header()
def get_cpu_data():
    """
    This function returns CPU data.
    """
    try:
        cpu_percent = psutil.cpu_percent()
        logger.debug("cpu_percent  %s ", cpu_percent)
        return jsonify({"cpu_percent": cpu_percent})
    except requests.exceptions.HTTPError as http_err:
        # Log the error
        logger.error("An error occurred: %s", str(http_err))
        # Handle any exceptions that occur
        return jsonify({'message': 'An error occurred'})

@app.route("/data/memory")
@verify_request_header()
def get_memory_data():
    """
    This function returns Memory data.
    """
    try:
        free_memory = psutil.virtual_memory().free
        total_memory = psutil.virtual_memory().total
        memory_usage = (total_memory - free_memory) / total_memory * 100
        memory_data = {
            "free_memory": free_memory,
            "total_memory": total_memory,
            "memory_usage": memory_usage
        }
        return jsonify(memory_data)
    except requests.exceptions.HTTPError as http_err:
        # Log the error
        logger.error("An error occurred: %s", str(http_err))
        # Handle any exceptions that occur
        return jsonify({'message': 'An error occurred'})

@app.route("/data/containers/stats")
@verify_request_header()
def get_container_stats():
    """
    This function returns containers stats data.
    """
    try:
        # Connect to the Docker daemon
        client = docker.from_env()
        # Get a list of running containers
        containers = client.containers.list()
        # Collect stats for each running container
        container_stats = {}
        for container in containers:
            stats = container.stats(stream=False)
            container_stats[container.name] = stats
        # Return the container stats as JSON
        return jsonify(container_stats)
    except requests.exceptions.HTTPError as http_err:
        # Log the error
        logger.error("An error occurred: %s", str(http_err))
        # Handle any exceptions that occur
        return jsonify({'message': 'An error occurred'})

if __name__ == "__main__":
    # Get the port from the environment variable
    port = os.getenv('PORT')
    app.run(host='0.0.0.0', port=port)
