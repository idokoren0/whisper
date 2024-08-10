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
of itself. By default, sends that message after 100 seconds from start, can be configrued via env var in docker compose. Doesnt remove mounted files.

**WHISPER** is the main component of this project, and the supplied Receiver server, Sender and Terminator are examples for implemntations that you may use or replace however you see fit.

## Architecture

The project uses Docker to containerize the services. 
They communicate over a default docker bridge network and can be orchestrated using the supplied docker compose file.


### Prerequisites

- Docker
- Docker Compose (Optional)
- openssl (for certificate generation)

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/idokoren0/whisper.git
    cd whisper
    ```

2. **IMPORTANT** Create Certificates using the supplied guide under:
    whisper\certs\create_certs.txt
    OR
    Use the supplied bash script to generate them.
    ```
    cd whisper/certs
    apt-get install openssl 
    ./generate_certificate.sh
    ```
    Whisper wont work without them.
    After certificate createion, the certs dir should look like this:
    ```
    ── certs/
       ├── create_certs.txt
       ├── extfile.cnf
       ├── server.crt
       ├── server.csr
       └── server.key
    ```

3. Configure according to your needs:
    
    whisper can send data over tcp or http, and receive that configuration
    togther with a few other values in the config.yml file. For TCP transfer set DATA_TRANSFER to: tcp, for HTTP set it to http. For further detail refrence the configuration section of this guide.

4. Build and start the services:
    The docker compose file assuems a need for all of the services:
    Whisper, Sender, Receiver, Terminator.
    Feel free to comment out/remove the services you dont need from
    docker compsoe.
    To start the services:
    ```sh
    docker-compose up --build
    ```
    
## Configuration


Configuration for **whisper** is managed through the `config.yml` file, where you can define key parameters like listening ports, IP addresses, data transfer methods, and the termination message. For all other services, the configuration values are passed as ENV vars.

### Example Configuration for whisper (`config.yml`):
```yaml
listening_port: 12345
target_server: "receiver"
target_port: 8080
data_transfer: tcp # tcp OR http
terminator:
  terminator_message: "TERMINATE"
  terminator_ip: "172.19.0.5" # Insert IP here, NOT hostname
```

When changing data_transfer values, it's important to set the same
value as an Env Var for Receiver. To notify receiver to expect tcp
communication from whisper, you would set the docker compsoe as such:

```yaml
  receiver:
    build:
      context: .
      dockerfile: docker/Dockerfile.receiver
    ports:
      - "8080:8080"
    volumes:
      - ./scripts:/app/scripts
      - ./certs/server.crt:/app/server.crt
      - ./certs/server.key:/app/server.key
    environment:
      - DATA_TRANSFER=tcp  # Set to: tcp or http
```

## Usage
Afer startup of all of the services, communication will flow from sender
to whisper and then receiver automaticlly, and after the set time, terminator will send a terminate message to whisper. 
If you would like to only start whisper, it will just wait for any data to enrich and pass. You may test it by sending a message with curl without using sender:
```bash
curl telnet://0.0.0.0:12345 -T <(echo hello there)
```

## Testing
Unit Tests and E2E test are included in the project.
E2E test the flow of data from sender to reciver and checks the message was transferred through whisper.
Unit tests are lacking coverage of server, sender and terminator.
