# TCP编程: 客户端

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))
for data in [b'Michel', b'Tracy', b'Sarah']:
    # 发送数据
    s.send(data)
    print (s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()
#
# # 接受数据
# buffer = []
# while True:
#     d = s.recv(1024)
#     if d:
#         buffer.append(d)
#     else:
#         break
# data = b''.join(buffer)
#
# # 关闭连接
# s.close()
#
# header, html = data.split(b'\r\n\r\n', 1)
# print(header.decode('utf-8'))