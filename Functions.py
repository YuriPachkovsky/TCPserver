import os
import socket as s


def upload(connection):
    file_name = connection.recv(1024).decode()
    file = open("files/" + file_name, 'wb')
    if file:
        connection.send(b"Ok_Name")
    else:
        print("error")
    data = connection.recv(1024)
    size = int(str(data.decode('UTF-8', 'ignore')).strip())
    connection.send(b'Ok')
    while size > 0:
        download_data = connection.recv(1024)
        file.write(download_data)
        size -= len(download_data)
    file.close()
    return


def download(connection):
    file_name = connection.recv(1024).decode()
    try:
        file = open("files/" + file_name, "rb")
    except IOError:
        connection.send(b"No_File")
        return
    else:
        size = os.stat("files/" + file_name).st_size
        connection.send(bytes(str(size), 'UTF-8').strip())
        while True:
            data = connection.recv(1024)
            if data:
                break
        data = file.read(1024)
        while data:
            connection.send(data)
            data = file.read(1024)
        file.close()
        return


def exit(connection, socket):
    # connection.send(b'Ok')
    connection.shutdown(1)
    connection.close()
    socket.shutdown(1)
    socket.close()
    return


def keepalive(socket, after_idle_sec=1, interval_sec=2, max_fails=1):
    socket.setsockopt(s.SOL_SOCKET, s.SO_KEEPALIVE, 1)
    socket.setsockopt(s.IPPROTO_TCP, 9, after_idle_sec)
    socket.setsockopt(s.IPPROTO_TCP, 5, interval_sec)
    socket.setsockopt(s.IPPROTO_TCP, 6, max_fails)
