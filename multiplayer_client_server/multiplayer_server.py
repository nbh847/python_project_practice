import socket, select, threading
import time

host = '127.0.0.1'
port = 5963
addr = (host, port)

inputs = []
fd_names= {}

def who_in_room(who):
    name_list = []
    for k in who:
        name_list.append(who[k])
    return name_list

def conn():
    print ('running...')
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(addr)
    my_socket.listen(5)
    print ('waiting for connection....')
    return my_socket

def new_comming(my_socket, addr):
    print ('welcome %s:%s' % (addr))
    wel = '''welcome into the talking room . 
        please decide your name.....'''

    my_socket.send(wel.encode('utf-8'))
    name = my_socket.recv(1024)
    print ('name: {}'.format(name))
    inputs.append(my_socket)
    fd_names[addr[1]] = name.decode('utf-8')
    nameList = "Some people in talking room, they are %s" % (who_in_room(fd_names))
    for socks in inputs:
        socks.send(nameList.encode('utf-8'))

def new_leaving(my_socket, addr):
    print ('%s:%s leaving....' % addr)
    msg = '%s leaving the chating room.' % fd_names[my_socket]

    inputs.remove(my_socket)
    for socks in inputs:
        socks.send(msg.encode('utf-8'))

def tcplink(sock, addr):
    print ('Accept new connection from %s:%s...' % addr)
    if sock not in inputs:
        new_comming(sock, addr)
    # sock.send(('Welcome: %s:%s!' % addr).encode('utf-8'))

    # receive data
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data:
            break
        print ('data: {0}from : {1}'.format(data.encode('utf-8'), addr[1]))

        # 转发消息到所有的其他socket
        for user in inputs:
            if user is not sock:
                user.send(('[%s] says: %s' % (fd_names[addr[1]], data.decode('utf-8'))).encode('utf-8'))

    new_leaving(sock, addr)
    sock.close()
    print('Connection from %s:%s closed.' % addr)

def server_run():
    my_sock = conn()
    while True:
        sock, addr = my_sock.accept()
        my_thread = threading.Thread(target=tcplink, args=(sock, addr))
        my_thread.start()

if __name__ == '__main__':
    server_run()