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
    sentence = connectionSocket.recv(1024)
    print(sentence.decode())
    
    # Definindo funções dos camandos
    # Comando pwd
    def pwd_command():
        # Obtém o diretório atual
        current_dir = os.getcwd()
        connectionSocket.send(current_dir.encode())
        
    def ls_command():
        # Transforma a lista de arquivos em uma string
        file_list = '\n'.join(os.listdir())
        connectionSocket.send(file_list.encode())
        
    def cd_command(*args):
        new_dir = args[0]
        if os.path.isdir(new_dir):
            os.chdir(new_dir)
            current_dir = os.getcwd()
            connectionSocket.send(f'Current directory: {current_dir}'.encode())
        else:
            connectionSocket.send('Invalid directory'.encode())
    
    if sentence.decode() == 'exit':
        #connectionSocket.close()
        break
    
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
    else:
        connectionSocket.send('Invalid command'.encode())

# Fecha a conexão do socket após a resposta ter sido enviada
connectionSocket.close()
#serverSocket.close()