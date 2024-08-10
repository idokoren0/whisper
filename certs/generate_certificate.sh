#!/bin/bash

# Set the hostname; change 'receiver' to your needs.
HOSTNAME="receiver"

# Create a private key
openssl genpkey -algorithm RSA -out server.key

# Create a certificate signing request (CSR) with the correct hostname.
openssl req -new -key server.key -out server.csr -subj "/CN=$HOSTNAME"

# Create a configuration file for the extensions
cat > extfile.cnf <<EOL
subjectAltName = DNS:$HOSTNAME
EOL

# Create a self-signed certificate with the extensions
openssl x509 -req -in server.csr -signkey server.key -out server.crt -days 365 -extfile extfile.cnf

echo "Certificate and key have been generated successfully."