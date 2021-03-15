import socket as sok

socket = sok.socket()
socket.connect(('localhost', 8080))

while True:
    userInput = input('please enter a command: ')
    socket.send(userInput.encode())
    userCmd = userInput.split()[0].upper()
    msgReceived = socket.recv(4096).decode("utf-8")

    if msgReceived == 'QUIT':
        break

    elif msgReceived == 'LIST':
        msgReceived = socket.recv(4096).decode("utf-8")
        print(msgReceived)

    elif msgReceived == 'RETRIEVE':
        file = open('./client/' + str(userInput.split()[1]), 'w')
        msgReceived = socket.recv(4096).decode()
        file.write(msgReceived)
        file.close()
        print('Successfully retrieved ' + userInput.split()[1] + ' from server')

    elif msgReceived == 'STORE':
        socket.send('STORE'.encode())
        try:
            file = open(('./client/' + userInput.split()[1]), 'r')
        except FileNotFoundError:
            print(userInput.split()[1] + ' can not be found')
            socket.send('ERROR'.encode())
            continue

        socket.send(file.read().encode())
        file.close()
        print('Successfully sent ' + userInput.split()[1] + ' to server')

    elif msgReceived == 'CONNECT':
        socket = sok.socket()
        socket.connect((userInput.split()[1], int(userInput.split()[2])))

    else:
        print('Unknown Command')
        socket.send('ERROR'.encode())

socket.close()
print('client successfully terminated')
