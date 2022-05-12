""" 
Socket cliente 
"""

from socket import *

serverName = 'localhost'
serverPort = 12000

"""laço que em toda iteração faz uma nova conexão ao servidor, de modo que cada requisição
ocorra em uma nova conexão com o servidor(fizemos isso pois estavamos tendo problema com
múltiplas requisições em uma só conexão, tornado o programa instável)"""
while 1:
    #AF_INET = Endereços ipv4
    #SOCK_STREAM = Socket com protocolo TCP
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    print("*******MENU*******")
    print("1 - Requisitar o armazenamento de um arquivo")
    print("2 - Requisitar lista de arquivos disponíveis")
    print("3 - Requisitar um arquivo armazenado")
    print("4 - Encerrar programa")
    opcao = input("Opção desejada:")
    
    if opcao == '4':
        #encerra conexão
        clientSocket.close()
        break

    #envia ao servidor o serviço desejado
    clientSocket.send(opcao.encode()) 

    if opcao == '1': #envia um arquivo para ser armazenado no servidor
        nomeArquivo = input("Digite o nome do arquivo:")
        try:
            File = open(nomeArquivo,'rb') #abre o arquivo e o habilita para "leitura binária"
            clientSocket.send(nomeArquivo.encode()) #envia ao servidor o nome do arquivo
            clientSocket.recv(1) #aguarda confirmação do servidor
            for data in File.readlines():
                clientSocket.send(data) #envia linha a linha o arquivo ao servidor
            print("Arquivo enviado com sucesso")
        except FileNotFoundError: #captura o erro caso o arquivo não esteja no disco do cliente
            print("Arquivo não encontrado.")

    if opcao == '2': #solicita nomes dos arquivos armazenados
        while 1:
            nomeArquivo = clientSocket.recv(1024).decode() #recebe os nomes do servidor
            if not nomeArquivo:
                break
            else:
                clientSocket.send("1".encode()) #envia uma confirmação que recebeu o dado
            print(nomeArquivo)

    if opcao == '3': #recebe um arquivo armazenado no servidor
        nomeArquivo = input("Digite o nome do arquivo do servidor:")
        clientSocket.send(nomeArquivo.encode()) #envia o nome do arquivo desejado
        #recebe um sinal que representa o sucesso na abertura do arquivo no servidor
        mensagem = clientSocket.recv(1).decode() 
        if(mensagem == "1"):
            with open(nomeArquivo, "wb") as File: #cria o arquivo se não exisir e o abre para "escrita binária"
                #laço para receber do servidor os dados linha a linha do arquivo
               while 1:
                    data = clientSocket.recv(1024)
                    if not data:
                        break
                    File.write(data)
            print("Arquivo recebido com sucesso")
        else:
            print("Arquivo não encontrado no servidor")
    
    #encerra conexão
    clientSocket.close()
    print()