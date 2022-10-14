import socket 
import argparse, re
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", dest="target_host", help="url target argument")
args = parser.parse_args()

HOST = args.target_host
PORT = 80

# initialize socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print(urlparse(f'{HOST}'))
domain = urlparse(f'{HOST}').netloc

# socket connect
client.connect((domain,PORT))

# \r\n = CRLF
request = (f'GET / HTTP/1.1\r\nHost: {domain}\r\n\r\n')

# socket send
client.send(request.encode()) # convert to bytes

# socket receive
data = client.recv(1024)
response = data.decode("utf8")
#print(response)

title = re.findall(r"<title>(.*)</title>", response)[0]
print("Title: ", title[0:10])

#socket close
client.close()