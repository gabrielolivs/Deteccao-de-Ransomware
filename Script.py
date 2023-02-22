    #-- Importando bibliotecas
    import glob
    import json
    import csv
    import time

    #-- Função json_arq 'Função criada para ler os arquivos JSON de um determinado diretório e realizar o tratamento dos dados para a criação de uma tabela informativa'
    def json_arq(dir_arq):
	
        #-- Laço de repetição para a captura dos dados requeridos
        for file in dir_arq:

            print("Nome do arquivo: " + file) #-- Nome do arquivo

            #-- Realizando leitura do arquivo json
            with open(file,'r', encoding='utf8') as f: #-- Abrindo o arquivo em forma de leitura
                # Nome de cada coluna no CSV
                col = [] #-- Colunas
                col_aux = ['file_name','command_line', 'score_binary']
                col_count = [] #-- Número de registros
                numbers = []
                aux = []
				
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
                             print("Ja incluído + " + api)             
                        else:
                            col.append(api)
                        count9 = count9 + 1 #-- Incrementando contador
                    count8 = count8 + 1 #-- Incrementando contador 

                count = 0
                d = open('amostra20-2.csv', 'a', newline='', encoding='utf-8')
                w = csv.writer(d)
                w.writerow(col_aux+col)

                arquivo = open("apis_20-2.txt","a")

                #-- Laço de repetição para a leitura de arquivos JSON
                #-- O mesmo visa entrar no espaço em questão do arquivo JSON para a captura das informações que queremos coletar\n",
                for i in data['behavior']['processes']: #-- For 1
                    command_line = data['behavior']['processes'][count]['command_line'] #-- Comando utilizando pelo binário
                    score = data['info']['score']
                    print("========================================")
                    print("-> primeiro laço " + str(count))
                    print("========================================")
                    count2 = count
                    count3 = 0
                    for j in data['behavior']['processes'][count2]['calls']:
                    
                        print("Nome comando: " + command_line + "+ numero: +" + str(count2) + " ===" + "numero1: " + str(count3))
                        if api in col:
                            print("Contabilizando... " + api)
                            col_count.append(data['behavior']['processes'][count2]['calls'][count3]['api']+"\n")
                            arquivo.writelines(col_count)
                        else:
                            print("Não faz nada")
                        
                        print("Lista! *******")
                        print(col_count)
                        
                        col_count.clear()
                        count3 = count3 + 1
                        
                    lines = open('apis_20-2.txt','r').read().splitlines()
                    for name in col:
                        print(name + " = " + str(lines.count(name)))
                        numbers.append(lines.count(name))
                    
                    print("=========== PRINTANDO LINHAS ARQUIVO ================")
                    print(lines)

                    print("=========== PRINTANDO LISTA DE NÚMEROS ================")
                    print(numbers)

                    print("=========== PRINTANDO LISTA DE COLUNAS ================")
                    print(col)
                    #-- Inclui linha csv
                    w.writerow([command_line,]+numbers)
                    #-- Encrementador do contador para a leitura dos dados\n",
                    count = count + 1

                    print("=========== LIMPANDO LISTA DE NÚMEROS ================")
                    numbers.clear()
                    print(numbers)

                    time.sleep(2)
                    print("=========== LIMPANDO ARQUIVO ================")
                    #arquivo.truncate(0)
                    
                f.close()
                arquivo.close()
    #-- Função main
    def main():

        #-- Diretório dos arquivos JSON - Amostras Cuckoo Sandbox
        #-- Exemplo para rodar o script
        file_list = glob.glob('C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\tcc\\7\\reports\\report.json')

        #-- Chamada da função json_arq
        json_arq(file_list)

    #-- Inicio do programa
    if __name__ == '__main__':
        main() #-- Inicializando a função main
