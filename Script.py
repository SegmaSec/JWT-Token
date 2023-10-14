#!/usr/bin/env python3
from colorit import *
init_colorit()
import json
import hmac
import base64
import hashlib
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

PURPLE = 145,31,186
DEEPPINK=255,20,147
CYAN=0,247,255
WHITE=255, 255, 255
RED=255, 0,0
GREEN=0, 255, 0

lists = ["HS256", "HS512", "HS384"]
code = ["Encode","Decode"]
generating = ["default","generate"]
admin_value = ["true", "false", ""]

completer  = WordCompleter(code, ignore_case=True)
completer2  = WordCompleter(lists, ignore_case=True)
completer3 = WordCompleter(admin_value, ignore_case=True)
completer4 = WordCompleter(generating, ignore_case=True)


print(color("""

       ___       ________   ______      __            
      / / |     / /_  __/  /_  __/___  / /_____  ____ 
 __  / /| | /| / / / /      / / / __ \/ //_/ _ \/ __ \\
/ /_/ / | |/ |/ / / /      / / / /_/ / ,< /  __/ / / /
\____/  |__/|__/ /_/      /_/  \____/_/|_|\___/_/ /_/ 
                                                      
Drink Coffe, Enjoy Generate JWT          By 0xPwn1 / v1.2 

""",(PURPLE)))

x = prompt("[~] Choose (Encode \ Decode): ",completer=completer).lower()

def header():
    global alg
    global jwt_type

    alg = prompt(" > Enter Value alg: ",completer=completer2).upper()

    while not alg in lists:
        print(color(" => Only Alowed Functions Are:\n{}".format(" - ".join(lists)),(RED)))
        alg = prompt(" > Enter Value alg: ",completer=completer2).upper()

    jwt_type = input(" > Enter Value type: ")


def payload_Default():
    global admin, sub, name, iat
    sub = ""
    while type(sub) != int :
        try :
            sub = int(input(" > Enter Value sub: "))
        except:
            print(color(" => Only Number !!!!!",(RED)))
    name = ""
    while name == "":
        name = input(" > Enter Value name: ")
    admin = prompt(" > User is admin [true/false] (For Skip Click 'Enter'): ",completer=completer3).lower()
    while not admin in admin_value:
        print(color(" => Only Alowed Functions Are:\n{} - (Enter To Skip)".format(" - ".join(admin_value[:-1])),(RED)))
        admin = prompt(" > User is admin [true/false] (For Skip Click 'Enter'): ",completer=completer3).lower()

def playload_Generating():
    custom_payload = {}
    stop = 0
    while not stop:
        try:
            keyvalue = input("[~] Example Syntaxt => key:value (Enter To Stop): ")
            if keyvalue == '':
                break
            key, value = keyvalue.split(':')
            custom_payload[key] = value
        except:
            print(color("Error: Syntaxt => key:value",(RED)))
    return custom_payload

def signature():
    global secret
    secret = input(" > Enter Your Secret Key (Enter To Skip): ")


def encode_header():
    header1 = '{{"alg":"{}","typ":"{}"}}'.format(alg, jwt_type)
    en_header = base64.b64encode(header1.encode()).decode()
    return en_header


def encode_payload(admin):
    if admin in ('true', 'false'):
        payload1 = '{{"sub":"{}","name":"{}","admin":"{}"}}'.format(sub, name, admin)
    else:
        payload1 = '{{"sub":"{}","name":"{}"}}'.format(sub, name)
    en_payload = base64.b64encode(payload1.encode()).decode()
    return en_payload.replace("=", "")


def encode_payload_generation(payload):
    payload1 = json.dumps(payload, separators=(",", ":"))
    en_payload = base64.b64encode(payload1.encode()).decode()
    return en_payload.replace("=", "")


def HMACSHA_encode(alg, en_header, en_payload, secret):
    algos = {"HS256": hashlib.sha256, "HS512": hashlib.sha512, "HS384": hashlib.sha384}
    # Encode header and payload as bytes
    header_bytes = en_header.encode()
    payload_bytes = en_payload.encode()

    # Calculate the HMAC-SHA256 signature
    signature = hmac.new(secret.encode(), header_bytes + b'.' + payload_bytes, algos[alg])

    # Get the digest and encode as base64
    signature_base64 = base64.urlsafe_b64encode(signature.digest()).decode()

    return signature_base64.replace("=", "")


if x == 'encode':
    print(color("---------- Header -----------",(PURPLE)))
    header()
    encoded_header = encode_header()
    print("")
    print(color("---------- Payload -----------",(PURPLE)))
    payload = prompt(" > Generating Payload / or / Default Payload: ", completer=completer4)
    print(color(" [!] - Wanted: Order is Very Imported !!!",(RED)))
    print("")
    
    if payload == "default":
        print(color("""
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": "true"
}
""",(GREEN)))
        payload_Default()
        encoded_payload = encode_payload(admin)
    
    elif payload == "generate":
        encoded_payload = encode_payload_generation(playload_Generating())
    print("")
    print(color("---------- Signature -----------",(PURPLE)))
    
    signature()
    result = HMACSHA_encode(alg, encoded_header, encoded_payload, secret)
    print("")
    print(color("[$] Your Token is: ",(RED))+encoded_header + "." + encoded_payload + "." + result)

elif x == 'decode':
    jwt_token = input("[~] Enter Your JWT Token: ")
    print("")

    secret = None
    if len(jwt_token.split('.')) == 3:
        header2, payload2, secret = jwt_token.split('.')
    else:
        header2, payload2 = jwt_token.split('.')


    # Add padding if it's missing from the payload
    while len(payload2) % 4 != 0:
        payload2 += '='

    # Decode the header and payload from base64
    header2_bytes = base64.b64decode(header2.encode())
    payload2_bytes = base64.b64decode(payload2.encode())
    
    # Decode the bytes to UTF-8 strings
    header2_decoded = header2_bytes.decode('utf-8')
    payload2_decoded = payload2_bytes.decode('utf-8')
    
    print(color("---------- Decode JWT Token -----------",(PURPLE)))
    print(color("[+] Your Header is: ",(PURPLE))+header2_decoded)
    print(color("[+] Your Payload is: ",(PURPLE))+payload2_decoded)
    if secret:
        print(color("[+] Your Signature is: ",(PURPLE))+secret)
