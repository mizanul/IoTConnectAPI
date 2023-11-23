# IoTConnect API

IoTConnect API is a multi-container application, which provides endpoints to retrieve CPU, Memory, and docker containers stat information. The API is built using Python Flask and is served by nginx.


## Architecture Overview

The architecture of the application is based on the following flow:

1. A user makes an API request to an Nginx container.
2. The Nginx container acts as the entry point for a Flask application.
3. API provides the data based on request

## Requirements

To meet the architectural requirements, following steps are done:

1. docker-compose tool is used to manage multiple Docker containers from a single file.
2. Docker containers were configured with the following functionality:
   - Containers should restart in every scenario.
   - Containers should be able to communicate with each other and with services running on the Host OS over the local network.
   - The Flask API container should have privileged access.
   - Each container should have a defined name.
   - Secure network settings should be used for the containers from both the network access and traffic standpoint.
   - Nginx should use only the latest TLS version available.

## Implementation Details

### Nginx Container

To implement the specific details for the Nginx container, following steps are done:

1. Defined self-signed certificates for the Nginx container. These certificates should persist in the container after restarts or updates and should only be available for the Nginx container.
2. Defined specific log files for the Nginx container that should persist in the container after restarts or updates.
3. Configured the Nginx container to allow only the latest TLS version available.
4. Set the number of worker processes in the Nginx container to an optimum value for the system you are running it on.
5. Configure the Nginx container to behave as a reverse proxy to the Flask API container.

### Flask API Container

To implement the specific details for the Flask API container, following steps are done:

1. Added an endpoint "/data/memory" that allows retrieving the current RAM usage. 
2. Added an endpoint "/data/cpu" that allows retrieval of the current CPU usage. 
3. Added an endpoint "/data/containers/stats" that allows you to retrieve a list of the currently running containers with their running stats. 
4. Implemented a decorator to ensure that the Bearer token is present in the request header for each endpoint of the Flask API. However, it is important to note that this decorator only checks for the presence of the Bearer token in the header and does not verify the token itself. If you wish to verify the token against an internal or external Identity Provider, you can add additional code to the implementation.


## Prerequisites

Before running the API, make sure you have the following installed Python 3.x and docker tool:

To install Python 3.x, you can follow the link https://gist.github.com/MichaelCurrin/57caae30bd7b0991098e9804a9494c23

To install docker tool and docker-compose, you can follow the link https://dockerwebdev.com/tutorials/install-docker/

## Installation and running containers

1. Clone the repository:

```
git clone https://github.com/mizanul/IoTConnectAPI.git
```

2. Change into the project directory:

```
cd IoTConnectAPI
./run_containers.sh

```


## Usage

Open terminal (make sure curl is installed)

### Get CPU usage data
```
curl -H "Authorization: Bearer my-secret-key" -k https://localhost/data/cpu

```
### Get memory usage data
```
curl -H "Authorization: Bearer my-secret-key" -k https://localhost/data/memory

```
### Get container stats 

```
curl -H "Authorization: Bearer my-secret-key" -k  https://localhost/data/containers/stats

```

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## For local development and unit test 

Run the follwing commands:

```
./setup_env.sh
./run_test.sh

```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
