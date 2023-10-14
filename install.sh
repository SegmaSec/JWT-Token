#!/bin/bash

pip3 install -r requirements.txt
sudo mv Script.py /usr/local/bin/JWT-Token
sudo chmod +x /usr/local/bin/JWT-Token
sudo rm -rf ../JWT-Token

echo "JWT-Token is Installed !!!"