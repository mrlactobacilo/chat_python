import socket
import select
import sys

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
conn.connect((IP_address, Port))

while True:
    try:
        message = conn.recv(2048)
        if message:
            print( message)
            continue
            # message_to_send = "<" + addr[0] + "> " + message
            # broadcast(message_to_send, conn)
            # prints the message and address of the user who just sent the message on the server terminal
        else:
            print('Error')
    except Exception as e:
        print(e)
        break
    try:
        if select.select([sys.stdin, ], [], [])[0]:
            entrada = sys.stdin.readline()
            entrada = IP_address + ' says: ' + entrada
            conn.send(entrada)
            print(entrada)
            sys.stdout.flush()
            continue
    except Exception as e:
        print(e)
        break
conn.close()