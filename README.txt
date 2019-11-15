Chat em Python

Requisitos:
    Python 3.6 ou 2.7

Iniciando o servidor:
    Para iniciar o servidor basta abrir o terminal na pasta raíz do programa e executar o comando:

        sudo python3.6 chat_server.py <porta> --> para Python 3.6
        sudo python2.7 chat_server27.py <porta> --> para Python 2.7

    Após isso o servidor iniciará e ficará à espera de conexões

Conectando-se ao servidor:
    Para conectar-se ao servidor basta abrir o terminal na pasta raíz do programa e executar o comando:

        sudo python3.6 client.py --> para Python 3.6
        sudo python2.7 client27.py --> para Python 2.7

    Após isso o programa pedirá para entrar com o IP do servidor, porta do servidor e nome de usuário, bastando
    apenas informar os dados e teclar enter a cada informação. Por fim, o sistema exibirá uma mensagem
    de boas vindas ao chat, e para enviar mensagens basta apenas digitá-las e teclar enter.