from socket import *
import os

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
    # modifiedMessage = message.decode().upper()
    # modifiedMessage = 'AOPA BÃO'

    # Comando pwd
    def pwd_command():
        current_dir = os.getcwd()
        serverSocket.sendto(current_dir.encode(), clientAddress)

    # Comando ls
    def ls_command():
        file_list = "\n".join(os.listdir())
        serverSocket.sendto(file_list.encode(), clientAddress)

    # Comando cd
    def cd_command(*args):
        new_dir = args[1]
        print(new_dir)

        if os.path.isdir(new_dir):
            os.chdir(new_dir)
            current_dir = pwd_command()
            serverSocket.sendto(f"Current directory: {current_dir}".encode, clientAddress)
        else:
            serverSocket.sendto("Diretório inválido".encode(), clientAddress)

    # Comando scp
 
 
    command, *args = message.decode().strip().split()

    if command == 'pwd':     
        pwd_command()
    if command == 'ls':
        ls_command()
    if command == 'cd':
        cd_command(command)
    else:
        serverSocket.sendto("Comando invalido".encode(), clientAddress)

    # Enviando a mensagem modificada de volta para o cliente
    # serverSocket.sendto(modifiedMessage.encode(), clientAddress)
