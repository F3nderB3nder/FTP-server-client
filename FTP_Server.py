import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen()
(clientSocket, clientAddress) = server.accept()

while True:
    clientCmd = clientSocket.recv(4096).decode("utf-8").split()
    command = clientCmd[0].upper()

    if command == 'QUIT':
        clientSocket.send('QUIT'.encode())
        break

    elif command == 'LIST':
        clientSocket.send('LIST'.encode())
        files = ''
        for file in os.listdir('./archive'):
            files += (file + '\n')
        clientSocket.send(files.encode())
        print('List has been sent to the client.')
        continue

    elif command == 'RETRIEVE':
        clientSocket.send('RETRIEVE'.encode())
        try:
            file = open(('./archive/' + clientCmd[1]), 'r')
        except FileNotFoundError:
            clientSocket.send('ERROR'.encode())
            continue
        clientSocket.send(file.read().encode())
        file.close()
        print('Successfully sent file ' + clientCmd[1] + ' to client')
        continue

    elif command == 'STORE':
        clientSocket.send('STORE'.encode())
        msgReceived = clientSocket.recv(4096).decode()
        file = open(('./archive/' + clientCmd[1]), 'w')
        file.write(msgReceived)
        print('Successfully wrote ' + clientCmd[1] + ' to server')
        file.close()

    elif command == 'CONNECT':
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((clientCmd[1], int(clientCmd[2])))
        server.listen()
        clientSocket.send('CONNECT'.encode())
        clientSocket.close()
        (clientSocket, clientAddress) = server.accept()
        print('Successfully connected to port number: ' + clientCmd[2])
        continue

clientSocket.close()
print('Server has successfully terminated the connection with client')
