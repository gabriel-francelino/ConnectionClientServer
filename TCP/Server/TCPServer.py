# importando as bibliotecas necessárias
import socket, os

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

# Aguarda uma conexão de um cliente
connectionSocket, addr = serverSocket.accept()

while True:
    
    # Recebe a sentença enviada pelo cliente através da conexão
    sentence, _ = connectionSocket.recvfrom(1024)
    print(sentence.decode())
    
    # Definindo funções dos camandos
    # Comando pwd
    def pwd_command():
        # Obtém o diretório atual
        current_dir = os.getcwd()
        connectionSocket.send(current_dir.encode())
        
    # Comando ls
    def ls_command():
        # Transforma a lista de arquivos em uma string
        file_list = '\n'.join(os.listdir())
        connectionSocket.send(file_list.encode())
        
    # Comando cd
    def cd_command(*args):
        new_dir = args[0]
        if os.path.isdir(new_dir):
            os.chdir(new_dir)
            current_dir = os.getcwd()
            connectionSocket.send(f'Current directory: {current_dir}'.encode())
        else:
            connectionSocket.send('Invalid directory'.encode())
    
    # Comando scp
    def scp_command(*args):
        file_name = args[0]
        
        # Verificando se o arquivo existe
        if os.path.exists(file_name) and os.path.isfile(file_name):
            # Manda '1' se arquivo existir
            connectionSocket.send('1'.encode())
            print('Tem arquivo mano.')
            
            # Obtém o tamanho do arquivo e enviando para o cliente
            file_size = os.path.getsize(file_name)
            connectionSocket.send(str(file_size).encode())
            print(f'Tamanho do arquivo a ser enviado: {file_size}')
            
            # Tamanho máximo do pacote
            max_packet_size = 1400
            
            # Abrindo o arquivo para leitura binária
            file = open(file_name, 'rb')
            # Enviando os dados do arquivo para o cliente
            while file_size > 0:
                # Se o tamanho do arquivo for maior que o limite do pacote
                # será enviado a quantidade de dados max do pacote 
                if(file_size > max_packet_size):
                    file_data = file.read(max_packet_size)
                    connectionSocket.send(file_data)
                    # Espera confirmação do cliente
                    connectionSocket.recv(1024)
                    file_size -= max_packet_size
                # Se não, será enviado o tamanho que falta
                else:
                    file_data = file.read(file_size)
                    connectionSocket.send(file_data)
                    # Espera confirmação do cliente
                    connectionSocket.recv(1024)
                    file_size -= file_size
            file.close()
            print('Tá tudo entregue parceiro.')
            
            # Enviando uma confirmação para o cliente
            connectionSocket.send('Arquivo copiado com sucesso!'.encode())
        else:
            # Manda '0' se arquivo não existir
            connectionSocket.send('0'.encode())
            print('Não tem arquivo mano.')
            
            # Enviando uma confirmação para o cliente
            connectionSocket.send('Arquivo não encontrado!'.encode())
    
    # # Converte a sentença para letras maiúsculas
    # capitalizedSentence = sentence.upper()
    
    # # Envia a sentença modificada de volta ao cliente através da conexão
    # connectionSocket.send(capitalizedSentence)
    
    command, *args = sentence.decode().strip().split()
    args = args if len(args) > 0 else [' ']
    
    if(command == 'pwd'):
        pwd_command()
    elif(command == 'ls'):
        ls_command()
    elif(command == 'cd'):
        cd_command(*args)
    elif(command == 'scp'):
        scp_command(*args)
    elif(command == 'exit'):
        break
    else:
        connectionSocket.send('Invalid command'.encode())

# Fecha a conexão do socket após a resposta ter sido enviada
connectionSocket.close()
serverSocket.close()