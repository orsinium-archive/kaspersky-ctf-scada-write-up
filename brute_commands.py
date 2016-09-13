import socket

serv = ('119.81.178.102', 1337)
sock = socket.socket()
sock.connect(serv)

print(sock.recv(8192))
sock.send(b'a\n')
bad = sock.recv(8192)
print(bad)

from string import ascii_lowercase
from itertools import product

prev = b'0'[0]
f = open('cmds', 'w')
for cnt in range(3, 7):
	for cmd in product(ascii_lowercase, repeat=cnt):
		cmd = ''.join(cmd).encode()
		sock.send(cmd + b'\n')
		answer = sock.recv(8192)
		if not answer.startswith(b'Unknown command:'):
			print('!!!', cmd)
			f.write(str(cmd)+'\n')
			f.flush()
		if cmd[-3] != prev:
			print(cmd)
			prev = cmd[-3]
