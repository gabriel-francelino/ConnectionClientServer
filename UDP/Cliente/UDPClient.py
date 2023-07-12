# importando o módulo de soquete
import socket, os

# Definindo o nome do servidor e a porta
# Tem que alterar o serverName na hora de testar
serverName = 'localhost'
serverPort = 12000

# Criando um objeto de soquete UDP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Entrada dos comandos
    message = input('$: ')
    
    # O comando exit fecha o cliente
    if message == 'exit':
        break
    
    # Enviando a mensagem codificada para o servidor especificado pelo nome e porta
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    
    # Comando scp
    if message.split()[0] == 'scp':
        # Separando o comando dos argumentos
        command, *args = message.strip().split()
        clientSocket.sendto(args[0].encode(), (serverName, serverPort))
        
        # ### ACHO QUE É AO CONTRÁRIO, O SERVIDOR VAI COPIAR O ARQUIVO NO PATH DO CLIENTE
        # # Verificando se o arquivo existe
        # try:
        #     # Verificando se o arquivo existe
        #     if os.path.isfile(args[0]):
        #         # Enviando o nome do arquivo para o servidor
        #         clientSocket.sendto(args[0].encode(), (serverName, serverPort))
                
        #     # Abrindo arquivo para leiura em bytes
        #     with open(args[0], 'rb') as file:
        #         # Enviando o arquivo para o servidor
        #         file_data = file.read()
        #         clientSocket.sendto(file_data, (serverName, serverPort))
        # except FileNotFoundError:
        #     print('File not found.')
        #     continue
    
    # Recebendo a resposta modificada do servidor e o endereço do servidor
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    # Decodificando a mensagem recebida de bytes para string
    modifiedMessage = modifiedMessage.decode()

    # Imprimindo a mensagem modificada
    print(modifiedMessage)

# Fechando o soquete do cliente
clientSocket.close()
