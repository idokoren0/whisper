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
- **Terminator**: Sends a terminate message to whisper to remove all trace
of itself. By default, sends that message after 100 seconds from start, can be configrued via env var in docker compose.

**WHISPER** is the main component of this project, and the supplied Receiver server, Sender and Terminator are examples for implemntations that you may use or replace however you see fit.

## Architecture

The project uses Docker to containerize the services. 
They communicate over a default docker bridge network and can be orchestrated using the supplied docker compose file.


### Prerequisites

- Docker
- Docker Compose (Optional)

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/idokoren0/whisper.git
    cd whisper
    ```

2. Create Certificates using the supplied guide under:
    whisper\certs\create_certs.txt

3. Configure according to your needs:
    
    whisper can send data over tcp or http, and receive that configuration
    togther with a few other values in the config.yml file. For TCP transfer set DATA_TRANSFER to: tcp, for HTTP set it to http. For further detail refrence the configuration section of this guide.

4. Build and start the services:
    The docker compose file assuems a need for all of the services:
    Whisper, Sender, Receiver, Terminator.
    Feel free to comment out/remove the services you dont need from
    docker compsoe.
    ```sh
    docker-compose up --build
    ```
    
## Configuration

If supplied 
docker compose file is not used, it is important to supply the env
variable specified per service in the compose file.