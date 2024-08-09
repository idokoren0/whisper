# Whisper Project

Whisper is an Innovative data transmission system desigend to capture, enrich and transmit critical intelligence from essential source to a designeted server.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Setup](#setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [License](#license)

## Overview

Whisper facilitates the reception, processing, and transmission of data through a secure and modular setup. The primary components include:

- **Receiver**: Listens for incoming data on a specified port and handles data transmission using either TCP or HTTPS.
- **Whisper**: Processes the received data, enriches it, and prepares it for sending over TCP or HTTPS.
- **Sender**: Sends data to a designated target (Whisper).

Whisper is the main component of this project, and the supplied Receiver server and Sender are examples for implemntations that you may use or replace however you see fit.

## Architecture

The project uses Docker to containerize the services. 
They communicate over a docker network and can be orchestrated
using the supplied docker compose file.


### Prerequisites

- Docker

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/whisper.git
    cd whisper
    ```

2. Create Certificates using the supplied guide under:
    whisper\certs\create_certs.txt

3. Configure according to your needs:
    whisper can send data over tcp or http, and receive that configuration
    togther with a few other values in the config.yml file. When setting 
    "Use HTTP" to true or false, it's important to also set the value 
    accordingly in the enviornment variable for Receivers docker compose.

4. Build and start the services:
    ```sh
    docker-compose up --build
    ```
    