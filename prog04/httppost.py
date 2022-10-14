import socket 
import argparse, re
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", dest="target_host", help="url target login")
parser.add_argument("--user", dest="username", help="user for login")
parser.add_argument("--password", dest="password", help="password for login")
parser.usage = parser.format_help()
args = parser.parse_args()

HOST = args.target_host
PORT = 80
user = args.username
password = args.password

# initialize socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
domain = urlparse(f'{HOST}').netloc

# socket connect
client.connect((domain,PORT))
#cookieList = ["wordpress_test_cookie=WP+Cookie+check"]

body = f'log={user}&pwd={password}&wp-submit=Log+In'
request = ( f'POST /wp-login.php HTTP/1.1\r\n'
            f'Host: {domain}\r\n'
            f'Content-Type: application/x-www-form-urlencoded\r\n'
            f'Accept: text/html,application/xhtml+xml,application/xml\r\n'
            f'Content-Length: {len(body)}\r\n'
            f'Connection: close\r\n\r\n'
            f'{body}\r\n'
)

client.send(request.encode()) 
data = client.recv(8192)
response = data.decode("utf8")
#print (response)

cookie_response = re.findall(r"Set-Cookie: (wordpress_logged_in_.+?)\r\n", response)
if cookie_response:
    print(f"User {user} đăng nhập thành công ")
else:
    print(f"User {user} đăng nhập thất bại")

client.close()