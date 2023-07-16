# importando as bibliotecas necessárias
import socket

# Define a porta do servidor
serverPort = 12000

# Cria um socket TCP
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket ao endereço do servidor e porta
serverSocket.bind(('', serverPort))

# O socket entra em modo de escuta, permitindo uma conexão
serverSocket.listen(1)

# Imprime uma mensagem indicando que o servidor está pronto para receber conexões
print('The server is ready to receive')


while True:
    # Aguarda uma conexão de um cliente
    connectionSocket, addr = serverSocket.accept()
    
    # Recebe a sentença enviada pelo cliente através da conexão
    sentence = connectionSocket.recv(1024)
    
    # Converte a sentença para letras maiúsculas
    capitalizedSentence = sentence.upper()
    
    # Envia a sentença modificada de volta ao cliente através da conexão
    connectionSocket.send(capitalizedSentence)

    # Fecha a conexão do socket após a resposta ter sido enviada
    # o finally garante que o socket será fechado mesmo que ocorra uma exceção
    connectionSocket.close()