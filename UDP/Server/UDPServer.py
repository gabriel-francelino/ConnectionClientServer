# importando as bibliotecas necessárias
import socket, os
import time

# Definindo a porta do servidor
serverPort = 12000

# Criando um objeto de soquete usando o protocolo UDP
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

    # Comando pwd
    def pwd_command():
        current_dir = os.getcwd()
        serverSocket.sendto(current_dir.encode(), clientAddress)

    # Comando ls
    def ls_command():
        # Transforma a lista de arquivos em uma string
        file_list = '\n'.join(os.listdir())
        serverSocket.sendto(file_list.encode(), clientAddress)

    # Comando cd
    def cd_command(*args):
        # Se o parâmetro for menor que 1, file_name vai receber ' '
        new_dir = args[0] if len(args) > 0 else ' '

        # Verifica se o diretório existe e muda para ele se existir
        if os.path.isdir(new_dir):
            os.chdir(new_dir)
            current_dir = os.getcwd()
            serverSocket.sendto(f'Current directory: {current_dir}'.encode(), clientAddress)
        else:
            serverSocket.sendto('Invalid directory'.encode(), clientAddress)

    # Comando scp
    def scp_command():
        # Recebendo o nome do arquivo
        file_name, _ = serverSocket.recvfrom(2048)
        file_name = file_name.decode()

        
        # Verificando se o arquivo existe
        if os.path.exists(file_name) and os.path.isfile(file_name):
            # Manda '1' se arquivo existir
            serverSocket.sendto('1'.encode(), clientAddress)
            print('Tem arquivo mano.')

            # Obtem o tamanho do arquivo
            file_size = int(os.path.getsize(file_name))
            
            # Envia o tamanho do arquivo para o cliente
            serverSocket.sendto(str(file_size).encode(), clientAddress)
            
            # Tamanho máximo do pacote
            max_packet_size = 1400
            
            # Abrindo arquivo para leitura binária
            file = open(file_name, 'rb')
            # Enviando o arquivo para o servidor
            print(f'Tamanho do arquivo a ser enviado: {file_size}')
            while file_size > 0:
                #time.sleep(0.01)
                #print(f'falta: {file_size}')
                # Se o tamanho do arquivo for maior que o limite do pacote
                # será enviado o a quantidade de dados max do pacote
                if(file_size > max_packet_size):
                    file_data = file.read(max_packet_size)
                    serverSocket.sendto(file_data, clientAddress)
                    serverSocket.recvfrom(2048)
                    file_size -= max_packet_size
                # Se não, será enviado o tamanho que falta
                else:
                    file_data = file.read(file_size)
                    serverSocket.sendto(file_data, clientAddress)
                    serverSocket.recvfrom(2048)
                    file_size -= file_size
            file.close()
            print('Tá tudo entregue parceiro')

            # Enviando uma confirmação para o cliente
            serverSocket.sendto('Arquivo copiado com sucesso!'.encode(), clientAddress)
        else:
            # Manda '0' se arquivo não existir
            serverSocket.sendto('0'.encode(), clientAddress)
            print('Achei esse trem não')
            
            # Enviando uma confirmação para o cliente
            serverSocket.sendto('Arquivo não encontrado!!'.encode(), clientAddress)
        
            
        
 
    # Separando o comando dos argumentos
    command, *args = message.decode().strip().split()

    # Execução dos comando
    if command == 'pwd':     
        pwd_command()
    elif command == 'ls':
        ls_command()
    elif command == 'cd': # precisa verificar se tem argumentos
        cd_command(*args)
    elif command == 'scp':
        scp_command()
    else:
        serverSocket.sendto('Invalid command'.encode(), clientAddress)

