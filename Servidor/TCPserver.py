""" 
Socket servidor 
"""

from socket import *
import os

#Função que realiza os procedimentos iniciais para instanciar um Socket TCP na porta desejada
def inicializar_servidor(serverPort):
    #AF_INET = Endereços ipv4
    #SOCK_STREAM = Socket com protocolo TCP
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('localhost',serverPort)) 
    serverSocket.listen()
    return serverSocket
    
serverSocket = inicializar_servidor(12000)

print ("O servidor está pronto")

while 1:
    #accept() retorna uma tupla com o objeto Socket do cliente e seu endereço ipv4
    connectionSocket, addr = serverSocket.accept() 
    print("Conexão iniciada com", addr)

    #espera-se do Socket cliente um byte que representa qual serviço ele solicitou
    opcao = connectionSocket.recv(1).decode()

    if opcao == '1':
        print("Solicitação do cliente para armazenar um arquivo")

        nomeArquivo = connectionSocket.recv(1024).decode()

        #condição para evitar problemas ao abrir o arquivo
        if nomeArquivo != '':
            #envia uma confirmação ao cliente
            connectionSocket.send("1".encode())  
            #realiza a abertura do arquivo para "escrita binária"    
            with open(nomeArquivo, 'wb') as File:
                #laço para receber do cliente os dados linha a linha do arquivo
                while 1:
                    data = connectionSocket.recv(1024)
                    if not data:
                        break
                    #Escreve no arquivo do servidor os dados
                    File.write(data)
                print("Arquivo armazenado com sucesso")
        else:
            print("Ocorreu um erro")

    if opcao == '2':
        print("Solicitação do cliente para enviar a lista de arquivos armazenados")
        
        #os.listdir retorna uma lista dos arquivos armazenados no diretório atual
        listaArquivos = os.listdir(".") # '.' indica o diretório atual(que está armazenado a aplicação)
        listaArquivos.remove("TCPserver.py") #retira da lista o código fonte da aplicação
        if len(listaArquivos) == 0:  
            connectionSocket.send("Não há arquivos disponíveis no servidor".encode())
            print("Não há arquivos armazenados")
        else: 
            #percorre a lista, enviando ao cliente todos os nomes de arquivos, um de cada vez
            for i in range(len(listaArquivos)): 
                connectionSocket.send(listaArquivos[i].encode())
                connectionSocket.recv(1) #confirmação da aplicação cliente
            print("Lista enviada com sucesso")
 
    if opcao == '3':
        print("Solicitação do cliente para recuperar um arquivo do servidor")
        nomeArquivo = connectionSocket.recv(1024).decode() #recebe o nome do arquivo da aplicação cliente
        try:
            File = open(nomeArquivo, "rb")
            connectionSocket.send("1".encode()) #envia confirmação de sucesso na abertura do arquivo
            print("Arquivo encontrado no servidor")
            for data in File.readlines():
                connectionSocket.send(data) #envia linha a linha o arquivo ao cliente
            print("Arquivo enviado com sucesso")
        except FileNotFoundError: #captura o erro caso o arquivo não esteja no servidor
            connectionSocket.send("0".encode())
            print("Arquivo não encontrado no servidor")


    connectionSocket.close()
    print("Conexão encerrada")


