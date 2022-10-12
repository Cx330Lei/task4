import socket
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def post_login(url, username, password):
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    domain = urlparse(url).netloc                 #lấy domain
    addr = socket.gethostbyname(domain)           #lấy địa chỉ ip
    port = 80
    s.connect((addr, port))

    header = "POST /wp-login.php HTTP/1.1\r\nHost: "+domain+"\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nOrigin: "+url+"\r\nContent-Type: application/x-www-form-urlencoded\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nReferer: http://blogtest.vnprogramming.com/wp-login.php\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9\r\nCookie: wordpress_test_cookie=WP%20Cookie%20check\r\nConnection: close\r\nContent-Length: 123\r\n\r\n"
    header = header.encode()
    body = 'log='+username+'&pwd='+password+'&wp-submit=Log+In&redirect_to=http%3A%2F%2Fblogtest.vnprogramming.com%2Fwp-admin%2F&testcookie=1\r\n'
    body = body.encode('ascii')
    req = header + body
    s.sendall(req)

    data = []
    while True: 
        response = s.recv(4096)
        if not response: 
            break
        data.append(response)

    #lấy đường dẫn được redirect tới
    for i in data:
        soup = BeautifulSoup(i, 'html.parser')
        for kq in soup.find_all('div', attrs={"id":"login_error"}):
            check = kq.text
            if "username or password you entered is incorrect" in check:
                print("User "+username+" đăng nhập thất bại")
                s.close
                exit()
        print("User "+username+" đăng nhập thành công")
    s.close

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type= str, help='show content exploit')
    parser.add_argument('--user', type= str, help='show content exploit')
    parser.add_argument('--password', type= str, help='show content exploit')
    try:
        args = parser.parse_args() #biến các tham số được gửi vào từ CLI thành các thuộc tính của 1 object và trả về object đó
    except:
        parser.print_help()
    url = str(args.url)
    username = str(args.user)
    password = str(args.password)
    post_login(url, username, password)

