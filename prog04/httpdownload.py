#!/usr/bin/env python3 
import socket
import re
import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", dest='target_host', help="Host target")
parser.add_argument("--remote-file", dest='remotefile', help="path file to download")
args = parser.parse_args()

HOST = args.target_host
PORT = 80
remote_file = args.remotefile

def recv_basic(the_socket):
    total_data=[]
    data = the_socket.recv(8192)
    while (len(data) > 0):
        # if not data: break
        total_data.append(data)
        data = the_socket.recv(8192)
    data = b''.join(total_data)
    return data

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
domain = urlparse(f'{HOST}').netloc
client.connect((domain,PORT))
header =  ( f'GET /{remote_file} HTTP/1.1\r\n'
            f'Host: {domain}\r\n'
            f'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0\r\n'
            f'Accept: */*\r\n'
            f'Accept-Language: en-US,en;q=0.5\r\n'
            f'Accept-Encoding: gzip, deflate\r\n\r\n'
)

client.send(header.encode())
response = recv_basic(client)

if b"HTTP/1.1 200 OK" in response:
    len_file = re.findall(b"Content-Length: ([0-9]+)\r\n", response)[0].decode()
    print("Kích thước file: " + len_file + " bytes")

    reply = b''
    headers =  reply.split(b'\r\n\r\n')[0]
    image = reply[len(headers)+4:]
    file_name = remote_file.split("/")[-1]
    f = open(f"images/{file_name}", "wb")
    f.write(image)
    f.close()
else:
    print("Không tồn tại file ảnh.")
    exit()
