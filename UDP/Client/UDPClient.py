# importando o módulo de soquete
import socket, os, sys

# Verifica se o número de argumentos está correto
if len(sys.argv) != 2:
    print("Usage: python script_name.py server_name")
    exit(1)

# Obtém o nome do servidor a partir do argumento fornecido
serverName = sys.argv[1]

# Definindo o nome do servidor e a porta
#serverName = 'localhost'
serverPort = 12000

# Criando um objeto de soquete UDP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Entrada dos comandos
    message = input('$: ')
    
    # O comando exit fecha o cliente
    if message == 'exit':
        break
    
    # Enviando o comando para o servidor especificado pelo nome e porta
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    
    # Comando scp
    if message.split()[0] == 'scp':
        # Separando o comando dos argumentos
        command, *args = message.strip().split()

        # Se o parâmetro for menor que 1, file_name vai receber ' '
        file_name = args[0] if len(args) > 0 else ' '
        clientSocket.sendto(file_name.encode(), (serverName, serverPort))


        #vai ter um if aqui pra ver se o arquivo existe
        file_found, _ = clientSocket.recvfrom(2048)
        if file_found.decode() == '1':
            # separando o nome do arquivo do caminho dele
            file_name = os.path.basename(file_name)
            print(file_name)
        
            # Recebendo o tamanho do arquivo
            file_size, _ = clientSocket.recvfrom(2048)
            file_size = int(file_size.decode())

            # Tamanho máximo do pacote
            max_packet_size = 1400

            # Recebendo os dados do arquivo do servidor
            file = open(file_name, 'wb')
            while file_size > 0:
                # Se o tamanho do arquivo for maior que o limite do pacote
                # será recebido o a quantidade de dados max do pacote 
                if(file_size > max_packet_size):
                    file_data, _ = clientSocket.recvfrom(max_packet_size)
                    file.write(file_data)
                    clientSocket.sendto('ACK'.encode(), (serverName, serverPort))
                    file_size -= max_packet_size
                # Se não, será recebido o tamanho que falta
                else:
                    file_data, _ = clientSocket.recvfrom(file_size)
                    file.write(file_data)
                    clientSocket.sendto('ACK'.encode(), (serverName, serverPort))
                    file_size -= file_size
            file.close()
            print('Chegou mais rápido que o SEDEX')
        
    
    # Recebendo a resposta modificada do servidor e o endereço do servidor
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    # Decodificando a mensagem recebida de bytes para string
    modifiedMessage = modifiedMessage.decode()

    # Imprimindo a mensagem modificada
    print(modifiedMessage)

# Fechando o soquete do cliente
clientSocket.close()
