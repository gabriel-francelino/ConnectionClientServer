# Importando as bibliotecas necessárias
import socket

# Definindo o nome do servidor e a porta
# Tem que alterar o serverName na hora de testar
serverName = 'localhost'
serverPort = 12000

# Criando um objeto de soquete TCP

while True:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta o socket ao endereço do servidor e porta
    clientSocket.connect((serverName, serverPort))

    # Solicita ao usuário uma sentença em letras minúsculas
    sentence = input('$: ')

    # O comando exit fecha o cliente
    if sentence == 'exit':
        clientSocket.close()
        break

    # Envia a sentença codificada para o servidor através do socket
    clientSocket.send(sentence.encode())

    # Recebe a resposta do servidor, com tamanho máximo de 1024 bytes
    modifiedSentence = clientSocket.recv(1024)

    # Imprime a resposta recebida do servidor
    print('From Server: ', modifiedSentence.decode())

    # Fecha a conexão do socket
    clientSocket.close()
