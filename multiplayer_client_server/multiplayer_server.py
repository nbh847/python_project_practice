import socket, select, threading

host = socket.gethostname()
port = 5963
addr = (host, port)

inputs = []
fd_names= {}

def who_in_room(w):
    name_list = []
    for k in w:
        name_list.append(k)
    return name_list

def conn():
    print ('running')
    my_socket = socket.socket()
    my_socket.bind(addr)
    my_socket.listen(5)
    return my_socket

def new_comming(my_socket):
    client, addr = my_socket.accept()
    print ('welcome %s %s' % (client, addr))
    wel = '''welcome into the talking room . 
        please decide your name.....'''
    try:
        client.send(wel)
        name = client.recv(1024)
        inputs.append(client)
        fd_names[client] = name
        nameList = "Some people in talking room, these are %s" % (who_in_room(fd_names))
        client.send(nameList)
    except Exception as e:
        print (e)

def server_run():

    my_socket = conn()
    inputs.append(my_socket)

    while True:
        r, w, e = select.select(inputs, [], [])
        for temp in r:
            if temp is my_socket:
                new_comming(my_socket)
            else:
                disconnect = False
                try:
                    data = temp.recv(1024)
                    data = fd_names[temp] + ' say: ' + data
                except socket.error:
                    data = fd_names[temp] + ' leave the room '
                    disconnect = True

            if disconnect:
                inputs.remove(temp)
                print (data)
                for other in inputs:
                    if other != my_socket and other != temp:
                        try:
                            other.send(data)
                        except Exception as e:
                            print (e)
                del fd_names[temp]

            else:
                print (data)

                for others in inputs:
                    if others != my_socket and others != temp:
                        try:
                            other.send(data)
                        except Exception as e:
                            print(e)


if __name__ == '__main__':
    server_run()