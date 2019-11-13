'''
Server python
Este código deve ser executado para iniciar o server, que ficará esperando por conxões e retransmitirá em
broadcast todas as mensagens enviadas pelos usuários conectados
'''

import socket
import threading
import sys

'''
Função resonsável por retornar o IP da máquina que está rodando o script
'''
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

'''
Função responsável por cada conexão, imprimindo a mensagem na tela do server e retransmitindo 
as mensagens recebidas 
'''
def clientthread(conn, addr):
    # enviando uma mensagem de boas vindas ao usuário que se conectou
    conn.send('Welcome to this chatroom!')

    while True:
            try:
                # Fica "ouvindo" a conexão conn à espera de pacotes enviados por ela
                message = conn.recv(2048)
                if message:
                    # Se um pacote for recebido, e a mensagem não for nula, a mesma será impressa na tela
                    print("<" + addr[0] + "> " + message)

                    # em seguida será adicionado o endereço do usuário que a enviou
                    message_to_send = "<" + addr[0] + "> " + message

                    # e por fim a mesma é re-transmitida para todos os usuários conectados no server
                    broadcast(message_to_send, conn)
                else:
                    # Se a mensagem for nula, o que corresponde a uma conexão instável, remove-se a conexão do server
                    remove(conn)
            except:
                continue


'''
Função responsável por transmitir em broadcast uma mensagem para todas as conexões da lista de usuários conectados
exceto para o próprio usuário que a enviou
'''
def broadcast(message,connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)


'''
Função responsável por remover uma conexão da lista de usuários conectados
'''
def remove(connection):
    if connection in clients:
        clients.remove(connection)


# criando um socket para a conexão
# AF_INET : define a família de IP que será utilizado (AF_ de Address Family)
# SOCK_STREAM : define o tipo de conexão do socket, sendo este utilizado para TCP e SOCK_DGRAM para uma conexão UDP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Aqui definimos que o kernel deve reutilizar essa porta mesmo que esteja no estado de TIME_WAIT.
# Isso pode ser útil ao reiniciarmos o server e o socket continuar ativo.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 2:
    print("Por favor, digite após o nome do script a porta desejada!")
    exit()
IP_address = str(get_ip_address())
Port = int(sys.argv[1])

# Vinculando o socket server a porta especificada. O lado client deve estar ciente desses valores
server.bind((IP_address, Port))

# Permitindo até 10 conexões
server.listen(10)

clients=[]

while True:
    print("IP do server: " + IP_address)
    print("Porta do server: " + str(Port))
    print("Aguardando conexões...")

    # Aceitando uma conexão. São retornados 2 parâmetros:
    # conn: objeto socket para a conexão do usuário que acabou de conectar
    # addr: endereço IP do usuário que acabou de conectar
    conn, addr = server.accept()

    # Adicionando o socket à lista de usuários conectados
    clients.append(conn)

    # Imprimindo na tela o endereço de quem conectou-se
    print(addr[0] + " conectou-se ao server")

    # Cria uma thread individual para cada novo usuário conectado
    threading.Thread(clientthread(conn, addr))

conn.close()
server.close()