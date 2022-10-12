import socket
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_title(url):
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    domain = urlparse(url).netloc 
    addr = socket.gethostbyname(domain)
    port = 80
    s.connect((addr, port))
    s.send(b'GET / HTTP/1.1\r\nHost: blogtest.vnprogramming.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n\r\n')
    data = []
    while True: 
        response = s.recv(4096)
        if not response: 
            break
        data.append(response)

    for i in data:
        soup = BeautifulSoup(i, 'html.parser')
        title = soup.find('h1')
        if title != None:
            print("Title: ",title.contents[0])
            s.close

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type= str, help='show content exploit')
    try:
        args = parser.parse_args() #biến các tham số được gửi vào từ CLI thành các thuộc tính của 1 object và trả về object đó
    except:
        parser.print_help()
    url = str(args.url)
    get_title(url)