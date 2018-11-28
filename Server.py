import socket
import datetime
import re
import Functions

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 3000))
sock.listen(1)
connection, address = sock.accept()

while True:
    try:
        data = connection.recv(4096).decode()
        if re.match(r'exit', data):
            Functions.exit(connection, sock)
            break
        elif re.match(r'echo ', data):
            message = (re.sub(r'echo ', '', data)).strip()
            connection.sendall((message + '\n').encode())
        elif re.match(r'time', data):
            connection.send((datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n').encode())
            continue
        elif re.match(r'upload', data):
            Functions.upload(connection)
            continue
        elif re.match(r'download', data):
            Functions.download(connection)
            continue
        else:
            connection.send(b'Invalid command. Please enter: echo, time, exit\n')
    except OSError or TimeoutError:
        print("no connection ")
        connection, address = sock.accept()
        continue
