#!/bin/bash

pip3 install -r requirements.txt
sudo mv Script.py /usr/local/bin/jwt-token
sudo chmod +x /usr/local/bin/jwt-token
sudo rm -rf ../JWT-Token && cd ..

echo "JWT-Token is Installed !!!"
