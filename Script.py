#-- Importando bibliotecas
import glob
import json
import csv
import os

def captura_colunas(dir_list):
    """
    Função que lê uma lista de arquivos JSON e retorna uma lista das colunas a serem incluídas no arquivo CSV de saída
    """
    colunas = []
    for arquivo in dir_list:
        with open(arquivo, 'r', encoding='utf8') as f:
            # Leitura do arquivo JSON
            data = json.load(f) 
            for i in data['behavior']['processes']:
                for j in i['calls']:
                    api = j['api']
                    if api not in colunas:
                        colunas.append(api)
    return colunas
        
#-- Função json_arq 'Função criada para ler os arquivos JSON de um determinado diretório e realizar o tratamento dos dados para a criação de uma tabela informativa'
def json_arq(dir_arq, colunas):
    with open('Data-set-TesteTCLimpos.csv', 'a', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        col_aux = ['command_line', 'score_binary']
        writer.writerow(col_aux + colunas)
        
        for arquivo in dir_arq:
            print("Nome do arquivo: " + arquivo) #-- Nome do arquivo
            with open(arquivo,'r', encoding='utf8') as f:
                #-- Instanciando uma variável que recebera a leitura do arquivo JSON
                data = json.load(f) 	
                for i, process in enumerate(data['behavior']['processes']):
                    # Comando utilizado pelo binário
                    command_line = process['command_line']
                    # Score do binário
                    score = data['info']['score']
                    print("========================================")
                    print("-> Processo " + str(i))
                    print("========================================")
                    calls = [call['api'] for call in process['calls']]
                    numeros = [calls.count(coluna) for coluna in colunas]
                    writer.writerow([command_line, score] + numeros)

#-- Função main
def main():

    #-- Diretório dos arquivos JSON - Amostras Cuckoo Sandbox
    #-- Exemplo para rodar o script
    file_list = glob.glob('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\tcc\\7\\reports\\Codigo - SEMISH\\amostraslivres\\Ryuk\\*.json')

    #-- Chamada da função captura_colunas para obter as colunas a serem utilizadas no arquivo CSV
    colunas = captura_colunas(file_list)
    print(colunas)
    print("\n")
    print('Quantidade de colunas ==> ' + str(len(colunas)) + ' <==')
    print("-========================================================-")

    json_arq(file_list, colunas)

#-- Inicio do programa
if __name__ == '__main__':
    main() #-- Inicializando a função main
