from socket import socket, SOCK_DGRAM, AF_INET

# Definindo o nome do servidor e a porta
# Tem que alterar o serverName na hora de testar
serverName = 'localhost'
serverPort = 12000

# Criando um objeto de soquete UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Solicitando que o usuário insira uma frase em letras minúsculas
message = input('Input lowercase sentence:')

# Enviando a mensagem codificada para o servidor especificado pelo nome e porta
clientSocket.sendto(message.encode(), (serverName, serverPort))

# Recebendo a resposta modificada do servidor e o endereço do servidor
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# Decodificando a mensagem recebida de bytes para string
modifiedMessage = modifiedMessage.decode()

# Imprimindo a mensagem modificada
print(modifiedMessage)

# Fechando o soquete do cliente
clientSocket.close()
