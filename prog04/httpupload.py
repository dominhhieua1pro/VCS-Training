#!/usr/bin/env python3
import socket
import argparse, re
from urllib.parse  import urlparse
import magic

parser = argparse.ArgumentParser()
parser.add_argument("--url",dest="target_url", help="url argument")
parser.add_argument("--user",dest="username", help="user to login")
parser.add_argument("--password",dest="password", help="password to login")
parser.add_argument("--local-file",dest="localfile", help="path file to upload")
parser.usage = parser.format_help()
args = parser.parse_args()

HOST = args.target_url
PORT = 80
user = args.username
password = args.password
localfile = args.localfile

def recvResponse(client, request):
    client.sendall(request.encode())         
    response = ""
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
        except socket.timeout:
            break
        response += data.decode()
    return response

def post(client,request):
    client.sendall(request)         
    response = ""
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
        except socket.timeout:
            break
        response += data.decode()
    client.close()
    return response

def getCookie(listCookie):
    cookieString = ""
    for cookie in listCookie:
        cookieString += cookie + '; '
    cookieString = cookieString[:-2]
    return cookieString

def getCookieUpdate(listCookie, response):
    newCookies = re.findall(r"Set-Cookie: (.*?)[;|\r\n]", response)
    for cookie in newCookies:
        if cookie not in listCookie:
            listCookie.append(cookie)
    if not newCookies:
        return 0
    else:
        return 1

def readFileImage(filename, mod):
    with open(filename, mode=mod) as f:
        return f.read()
mime = magic.Magic(mime=True)
read_file = readFileImage(localfile, "rb")

# check user login?
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    domain = urlparse(f'{HOST}').netloc
    #print(domain)

    # socket connect
    client.connect((domain,PORT))
    listCookie = ["wordpress_test_cookie=WP+Cookie+check"]
    
    body = f'log={user}&pwd={password}&wp-submit=Log+In'
    request = ( f'POST /wp-login.php HTTP/1.1\r\n'
                f'Host: {domain}\r\n'
                f'Content-Type: application/x-www-form-urlencoded\r\n'
                f'Accept: text/html,application/xhtml+xml,application/xml\r\n'
                f'Content-Length: {len(body)}\r\n'
                f'Cookie: {getCookie(listCookie)}\r\n'
                f'Connection: keep-alive\r\n\r\n'
                f'{body}\r\n'
    )

    client.send(request.encode())
    response = recvResponse(client,request)
    
    cookie_response = re.findall(r"Set-Cookie: (wordpress_logged_in_.*?)\r\n", response)
    # if cookie_response:
    #     print(f"User {user} đăng nhập thành công ")
    # else:
    #     print(f"User {user} đăng nhập thất bại")
    
    getCookieUpdate(listCookie, response)

# get _wpnonce
request = (
        f'GET /wp-admin/media-new.php/ HTTP/1.1\r\n'
        f'Host: {domain}\r\n'
        f'Upgrade-Insecure-Requests: 1\r\n'
        f'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0\r\n'
        f'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*\r\n'
        f'Cookie: {getCookie(listCookie)}\r\n'
        f'Connection: close\r\n'
        f'\r\n'
        )

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((domain,PORT))
    response = recvResponse(client, request)
    getCookieUpdate(listCookie, response)
    
params = re.search('"multipart_params":.*_wpnonce":"[0-9a-z]+"', response)
wp_nonce = re.search('(?<=_wpnonce":")[a-z0-9]{10}', params.group(0))
wp_nonce = wp_nonce.group(0)

file_name = localfile.split("\\")[-1]
request_body1 = (
        '-----------------------------335679337115370071493285990705\r\n' # WebKitFormBoundaryXXX
        f'Content-Disposition: form-data; name="async-upload"; filename="{file_name}"\r\n'
        f'Content-Type: {mime.from_file(localfile)}\r\n\r\n')
        
request_body2 = ('\r\n'
        f'-----------------------------335679337115370071493285990705\r\n'
        f'Content-Disposition: form-data; name="html-upload"\r\n'
        f'\r\n'
        f'Upload\r\n'
        f'-----------------------------335679337115370071493285990705\r\n'
        f'Content-Disposition: form-data; name="post_id"\r\n'
        f'\r\n'
        f'0\r\n'
        f'-----------------------------335679337115370071493285990705\r\n'
        f'Content-Disposition: form-data; name="_wpnonce"\r\n'
        f'\r\n'
        f'{wp_nonce}\r\n'
        f'-----------------------------335679337115370071493285990705\r\n\r\n'
        f'Content-Disposition: form-data; name="_wp_http_referer"\r\n'
        f'/wp-admin/media-new.php\r\n'
        f'-----------------------------335679337115370071493285990705--\r\n'
)
body = b''.join([request_body1.encode(),read_file,request_body2.encode()])
request = (
        f'POST /wp-admin/media-new.php/ HTTP/1.1\r\n'
        f'Host: {domain}\r\n'
        f'Cache-Control: max-age=0\r\n'
        f'Content-Length: {len(body)}\r\n'
        f'Upgrade-Insecure-Requests: 1\r\n'
        f'Content-Type: multipart/form-data; boundary=---------------------------335679337115370071493285990705\r\n'
        f'User-Agent: User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0\r\n'
        f'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*\r\n'
        f'Accept-Encoding: gzip, deflate\r\n'
        f'Accept-Language: en-US,en;q=0.9\r\n'
        f'Cookie: {getCookie(listCookie)}\r\n'
        f'Connection: close\r\n\r\n'
)
request = b''.join([request.encode(),body])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((domain,PORT))
    response = post(client, request)

    # find path upload file
    if "Upload-Attachment-ID" in response:
        attachment_id = response.split("\r\n")[7].split(" ")[1]
        path_url = re.compile('<p class="attachment"><a href=\'(.*)\'',flags=0)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        client.connect((domain,PORT))
        request = (
                f'GET /?attachment_id={attachment_id} HTTP/1.1\r\n'
                f'Host: {domain}\r\n'               
                f'Accept: text/html, */*; q=0.01\r\n'
                f'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0\r\n'              
                f'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
                f'Accept-Language: en-US,en;q=0.9\r\n'
                f'Cookie: {getCookie(listCookie)}\r\n'
                f'Connection: close\r\n\r\n'
                f'Upgrade-Insecure-Requests: 1'                
        )
              
        response = recvResponse(client, request)
        # Returns a list containing all matches
        print("Upload success. File upload url: " + path_url.findall(response)[0]) 
    else: print("Upload failed!")
