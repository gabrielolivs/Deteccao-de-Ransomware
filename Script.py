    #-- Importando bibliotecas
    import glob
    import json
    import csv
    import time
    import os

    def captura_coluna(dir_list):
        print("Lendo => ")
        col = []
        print("+========================================================+")
        for file in dir_list:
            print("Nome do arquivo: " + file) #-- Nome do arquivo
            print("++++++++")
            with open(file,'r', encoding='utf8') as f: #-- Abrindo o arquivo em forma de leitura
                
                #-- Instanciando uma variável que recebera a leitura do arquivo JSON
                data = json.load(f) 
                count8 = 0
                
                #-- Contador para pegar o número de api's que foram chamadas
                for i in data['behavior']['processes']:

                    count9 = 0 #-- Contador para a coleta dos elementos do termo calls
                    api = ""
                    for i in data['behavior']['processes'][count8]['calls']:
                        api = data['behavior']['processes'][count8]['calls'][count9]['api']
                        if api in col:
                            pass #--  Irá dar continuidade no loop (A api já está na lista de colunas)     
                        else:
                            col.append(api)
                            
                        count9 = count9 + 1 #-- Incrementando contador
                        
                    count8 = count8 + 1 #-- Incrementando contador
        f.close()
        return col
        
    #-- Função json_arq 'Função criada para ler os arquivos JSON de um determinado diretório e realizar o tratamento dos dados para a criação de uma tabela informativa'
    def json_arq(dir_arq,result_features):
	
        #-- Laço de repetição para a captura dos dados requeridos
        for file in dir_arq:

            print("Nome do arquivo: " + file) #-- Nome do arquivo

            #-- Realizando leitura do arquivo json
            with open(file,'r', encoding='utf8') as f: #-- Abrindo o arquivo em forma de leitura
                # Nome de cada coluna no CSV
                col = result_features #-- Colunas
                col_aux = ['command_line', 'score_binary']
                col_count = [] #-- Número de registros
                numbers = []
                aux = []
                
                #-- Instanciando uma variável que recebera a leitura do arquivo JSON
                data = json.load(f) 	
                
                count = 0
                d = open('Data-set-RyukLimpos.csv', 'a', newline='', encoding='utf-8')
                w = csv.writer(d)
                w.writerow(col_aux+col) 
                
                arquivo = open("ap1_testeatt.txt","a")

                #-- Laço de repetição para a leitura de arquivos JSON
                #-- O mesmo visa entrar no espaço em questão do arquivo JSON para a captura das informações que queremos coletar",
                for i in data['behavior']['processes']: #-- For 1
                    command_line = data['behavior']['processes'][count]['command_line'] #-- Comando utilizando pelo binário
                    score = data['info']['score']
                    print("========================================")
                    print("-> Laço " + str(count))
                    print("========================================")
                    count2 = count
                    count3 = 0

                    for j in data['behavior']['processes'][count2]['calls']:
                        #-- print("Adicionando =>  numero: " + str(count2) + " === " + "numero1: " + str(count3) + " => " + data['behavior']['processes'][count2]['calls'][count3]['api']+"\n")
                        arquivo.writelines(data['behavior']['processes'][count2]['calls'][count3]['api']+"\n") 
                        count3 = count3 + 1
                    count = count + 1
                    
                    for name in result_features:
                        with open('ap1_testeatt.txt','r') as file:
                            ocorrencias = file.read().count(name)
                        print(name + " = " + str(ocorrencias))
                        numbers.append(ocorrencias)
                        
                    print(numbers)
                    w.writerow([command_line,score]+numbers)
                    
                    with open('ap1_testeatt.txt','w') as fil:
                        fil.write('')
                    numbers.clear()
                    
                d.close()
                f.close()
                arquivo.close()
                
    #-- Função main
    def main():

        #-- Diretório dos arquivos JSON - Amostras Cuckoo Sandbox
        #-- Exemplo para rodar o script
        file_list = glob.glob('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\tcc\\7\\reports\\Codigo - SEMISH\\amostraslivres\\Ryuk\\*.json')

        #-- Chamada da função json_arq
        result_features = captura_coluna(file_list)
        print(result_features)
        print("\n")
        print('Quantidade de featuers ==> ' + str(len(result_features)) + ' <==')
        print("-========================================================-")

        json_arq(file_list,result_features)

    #-- Inicio do programa
    if __name__ == '__main__':
        main() #-- Inicializando a função main
