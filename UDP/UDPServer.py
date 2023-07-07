from socket import *

# Definindo a porta do servidor
serverPort = 12000

# Criando um objeto de soquete usando o protocolo UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Vinculando o soquete do servidor a um endereço IP vazio e à porta especificada
serverSocket.bind(('', serverPort))

# Imprimindo uma mensagem para indicar que o servidor está pronto para receber conexões
print('The server is ready to receive')

# Loop principal para receber e processar as mensagens dos clientes
while True:
    # Recebendo uma mensagem e o endereço do cliente que enviou a mensagem
    message, clientAddress = serverSocket.recvfrom(2048)

    # Imprimindo a mensagem recebida do cliente
    print('Message received from client: ', message.decode())

    # Modificando a mensagem para letras maiúsculas
    modifiedMessage = message.decode().upper()
    modifiedMessage = 'AOPA BÃO'

    # Enviando a mensagem modificada de volta para o cliente
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
