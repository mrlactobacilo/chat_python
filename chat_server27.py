# -*- coding: utf-8 -*-
'''
Server python
Este codigo deve ser executado para iniciar o server, que ficara esperando por conexoes e retransmitira em
broadcast todas as mensagens enviadas pelos usuarios conectados
'''

import socket
import threading
import sys

'''
Funcao resonsavel por retornar o IP da maquina que esta rodando o script
'''
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

'''
Funcao responsavel por cada conexao, imprimindo a mensagem na tela do server e retransmitindo 
as mensagens recebidas 
'''
def clientthread(conn, addr):
    # enviando uma mensagem de boas vindas ao usuario que se conectou
    conn.send('Welcome to this chatroom!')

    while True:
            try:
                # Fica "ouvindo" a conexao conn a espera de pacotes enviados por ela
                message = conn.recv(2048)
                if message:
                    # Se um pacote for recebido, e a mensagem nao for nula, a mesma sera impressa na tela
                    print("<" + addr[0] + "> " + message)

                    # em seguida sera adicionado o endereco do usuario que a enviou
                    message_to_send = "<" + addr[0] + "> " + message

                    # e por fim a mesma e re-transmitida para todos os usuarios conectados no server
                    broadcast(message_to_send, conn)
                else:
                    # Se a mensagem for nula, o que corresponde a uma conexao instavel, remove-se a conexao do server
                    remove(conn)
            except Exception as e:
                print(e)
                continue


'''
Funcao responsavel por transmitir em broadcast uma mensagem para todas as conexoes da lista de usuarios conectados
exceto para o proprio usuario que a enviou
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
Funcao responsavel por remover uma conexao da lista de usuarios conectados
'''
def remove(connection):
    if connection in clients:
        clients.remove(connection)


# criando um socket para a conexao
# AF_INET : define a familia de IP que sera utilizada (AF_ de Address Family)
# SOCK_STREAM : define o tipo de conexao do socket, sendo este utilizado para TCP e SOCK_DGRAM para uma conexao UDP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Aqui definimos que o kernel deve reutilizar essa porta, mesmo que esteja no estado de TIME_WAIT.
# Isso pode ser util ao reiniciarmos o server e o socket continuar ativo.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Por favor, digite apos o nome do script, o IP e a porta desejada, ambos separados por um espaco.")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

# Vinculando o socket server a porta especificada. O lado cliente deve estar ciente desses valores
server.bind((IP_address, Port))

# Permitindo ate 100 conexoes
server.listen(100)

clients=[]

while True:
    print("IP do server: " + IP_address)
    print("Porta do server: " + str(Port))
    print("Aguardando conexoes...")

    # Aceitando uma conexao. São retornados 2 parametros:
    # conn: objeto socket para a conexao do usuario que acabou de conectar
    # addr: endereço IP do usuario que acabou de conectar
    conn, addr = server.accept()

    # Adicionando o socket a lista de usuarios conectados
    clients.append(conn)

    # Imprimindo na tela o endereço de quem conectou-se
    print(addr[0] + " conectou-se ao server")

    # Cria uma thread individual para cada novo usuario conectado
    threading.Thread(clientthread,(conn, addr))

conn.close()
server.close()