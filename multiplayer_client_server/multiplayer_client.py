import socket, select, threading

host = '127.0.0.1'

addr = (host, 5963)


def conn():
    s = socket.socket()
    s.connect(addr)
    return s


def lis(s):
    my = [s]
    while True:
        r, w, e = select.select(my, [], [])
        if s in r:
            try:
                print(s.recv(1024))
            except socket.error:
                print('socket is error')
                exit()


def talk(s):
    while True:
        try:
            info = input()
        except Exception as e:
            print('can\'t input')
            exit()
        try:
            s.send(info)
        except Exception as e:
            print(e)
            exit()


def main():
    my_sock = conn()

    # 接收欢迎消息:
    print(my_sock.recv(1024).decode('utf-8'))

    # 输入聊天内容，输入0则断开
    while True:
        content = input()
        if content != 'exit':
            # 发送数据:
            my_sock.send(content.encode('utf-8'))
            feadback = my_sock.recv(1024).decode('utf-8')
            print (feadback)
        else:
            print ('exit chating...')
            break
    my_sock.close()


if __name__ == '__main__':
    main()
