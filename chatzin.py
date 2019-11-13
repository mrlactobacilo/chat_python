import socket
import select
import threading
import sys


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def client_thread(conn, addr):
    while True:
        try:
            sockets_list = [sys.stdin, conn]
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
            for socks in read_sockets:
                if socks == conn:
                    message = conn.recv(2048)
                    print('<' + addr + '>' + message)
                else:
                    message = sys.stdin.readline()
                    conn.send(message)
                    sys.stdout.write("<You>")
                    sys.stdout.write(message)
                    sys.stdout.flush()
        except:
            print("Error")
            continue


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(10)

print('Digite o endereço IP da máquina que deseja se conectar:\n')
ip = str(sys.stdin.readline())

print('Digite a porta desejada:\n')
port = int(sys.stdin.readline())

err = server.connect_ex((ip, port))

if err == 0:
    print('Conexão bem sucedida...')
    threading.Thread(client_thread(server,ip))
    server.close()
else:
    print(get_ip_address())
    server.bind((get_ip_address(), port))
    server.listen(1)

    while True:
        print('Esperando conexão...')

        conn, addr = server.accept()

        print(addr[0] + " se conectou à sua máquina")

        threading.Thread(client_thread(conn, addr))

    conn.close()
    server.close()
