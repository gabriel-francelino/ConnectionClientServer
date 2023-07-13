# importando as bibliotecas necessárias
import socket, os

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
        new_dir = args[0]

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
        if os.path.exists(file_name):
            print('Tem arquivo mano.')

            # Obtem o tamanho do arquivo
            file_size = int(os.path.getsize(file_name))
            
            # Envia o tamanho do arquivo para o cliente
            serverSocket.sendto(str(file_size).encode(), clientAddress)
            
            # Tamanho máximo do pacote
            max_packet_size = 1500
            
            # Abrindo arquivo para leitura binária
            
            with open(file_name, 'rb') as file:
                # Enviando o arquivo para o servidor
                #file_data = file.read(1)
                byte = 0
                limite = file_size
                print(file_size)
                while file_size > 0: 
                    if(file_size > max_packet_size):
                        file_data = file.read(1500)
                        serverSocket.sendto(file_data, clientAddress)
                    else:
                        file_data = file.read(file_size)
                        serverSocket.sendto(file_data, clientAddress)
                    file_size -= 1500
                    print(file_size)
                print('Tá tudo entregue parceiro')
            #--------------------------------------------------
            # with open(file_name, 'rb') as file:
            #     # Enviando o arquivo para o servidor
            #     # Precisa trocar para para decrementar o tamanho do arquivo
            #     while True: 
            #         packet = file.read(max_packet_size)
            #         if not packet:
            #             break
            #         serverSocket.sendto(packet, clientAddress)
        else:
            print('Achei esse trem não')

        # Recebendo o conteúdo do arquivo em pacotes
        # file_data, _ = serverSocket.recvfrom(65536)
        
        # Salvando o arquivo no diretório desejado no servidor
        # teste para ver se estava copiando mesmo: file_name = '../Cliente/teste.txt'
        # with open(file_name, 'wb') as file:
        #     file.write(file_data)
            
        #print(f"File '{file_name}' received and saved.")
            
        # Enviando uma confirmação para o cliente
        serverSocket.sendto("File received.".encode(), clientAddress)
 
    # Separando o comando dos argumentos
    command, *args = message.decode().strip().split()

    # Execução dos comando
    if command == 'pwd':     
        pwd_command()
    elif command == 'ls':
        ls_command()
    elif command == 'cd':
        cd_command(*args)
    elif command == 'scp':
        scp_command()
    else:
        serverSocket.sendto('Invalid command'.encode(), clientAddress)

