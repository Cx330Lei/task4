import socket
import argparse
from urllib.parse import urlparse
import select

def httpdownload(url, urlF):
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    domain = urlparse(url).netloc                 #lấy domain
    addr = socket.gethostbyname(domain)           #lấy địa chỉ ip
    port = 80
    s.connect((addr, port))

    header = "GET "+urlF+" HTTP/1.1\r\nHost: "+domain+"\r\nAccept-Encoding: gzip, deflate\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\nAccept: */*\r\nAccept-Language: en-US,en;q=0.9\r\nConnection: close\r\nCache-Control: max-age=0\r\n\r\n"
    header = header.encode()
    s.sendall(header)

    response = b''
    while select.select([s], [], [], 3)[0]:
        data = s.recv(4096)
        if not data: 
            break
        response += data
    
    #lấy kích thước của ảnh
    decode_res = response.decode('ISO-8859-1')
    arr = decode_res.split("\r\n")
    for i in arr:
        if "HTTP/1.1" in i:
            status = int(i.split()[1])
            if status == 404:
                print("Không tồn tại file ảnh")
                exit()
    for i in arr:
        if "Content-Length" in i:
            print("Kích thước file ảnh: "+ i.split()[1] + " bytes")

    h = response.split(b'\r\n\r\n')[0]
    image = response[len(h)+4:]
    # lưu ảnh
    f = open('imageDownload.jpg', 'wb')
    f.write(image)
    s.close

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type= str, help='show content exploit')
    parser.add_argument('--remote_file', type= str, help='show url file')
    try:
        args = parser.parse_args() #biến các tham số được gửi vào từ CLI thành các thuộc tính của 1 object và trả về object đó
    except:
        parser.print_help()
    url = str(args.url)
    urlF = str(args.remote_file)
    httpdownload(url, urlF)

