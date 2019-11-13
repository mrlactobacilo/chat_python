import socket
import select
import threading
import sys


def mensagem():
    # Verifica se foi digitado algo
    if select.select([sys.stdin,],[],[],0.0)[0]:
        # Formata a string para mandar "Cliente: <entrada>"
        entrada = "Cliente: {}".format(sys.stdin.readline())
        entrada = entrada.encode('utf-8')

        return entrada
    return False


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setblocking(False)

print "Digite o IP"
ip = str(sys.stdin.readline())

print "Digite a porta desejada"
port = int(sys.stdin.readline())

try:
    while 1:
        try:
            msg, amigo = server.recvfrom(2048)
            msg = msg.decode('utf-8').rstrip()
            print "{}: {}".format(amigo[0], msg)
        except:
            pass
        try:
            entrada = mensagem()
            if(entrada != False):
                server.sendto(entrada, (ip,port))
        except KeyboardInterrupt:
            sys.exit("\nChat encerrado!")
    server.close()
except Exception as e:
    print "O erro foi {}".format(erro)
    server.close
''' 

err = server.connect_ex((ip, port))
if err == 0:
    print "Conexao bem sucedida..."
    client_thread(server,ip)
    server.close()
else:
    print get_ip_address()
    server.bind((get_ip_address(), port))
    server.listen(10)

    while True:
        print 'Esperando conexao...'

        conn, addr = server.accept()

        print addr[0] + " se conectou a sua maquina"

        client_thread(conn, addr)

    conn.close()
    server.close()
'''
