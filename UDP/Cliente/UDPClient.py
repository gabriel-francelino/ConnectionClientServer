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

        # separando o nome do arquivo do caminho dele
        file_name = os.path.basename(args[0])
        print(file_name)

        # Recebendo o tamanho do arquivo
        file_size, _ = clientSocket.recvfrom(2048)
        file_size = int(file_size.decode())

        # Tamanho máximo do pacote
        max_packet_size = 1500

        # Recebendo os dados do arquivo do servidor
        with open(file_name, 'wb') as file:
            while file_size > 0:
                # Se o tamanho do arquivo for maior que o limite do pacote
                # será recebido o a quantidade de dados max do pacote 
                if(file_size > 0):
                    file_data, _ = clientSocket.recvfrom(max_packet_size)
                    file.write(file_data)
                # Se não, será recebido o tamanho que falta
                else:
                    file_data, _ = clientSocket.recvfrom(file_size)
                    file.write(file_data)
                file_size -= max_packet_size
            print('Chegou mais rápido que o SEDEX')
    
    # Recebendo a resposta modificada do servidor e o endereço do servidor
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    # Decodificando a mensagem recebida de bytes para string
    modifiedMessage = modifiedMessage.decode()

    # Imprimindo a mensagem modificada
    print(modifiedMessage)

# Fechando o soquete do cliente
clientSocket.close()
