# Um Estudo Acerca da Seleção de Features para a Detecção dos Ransomwares WannaCry, Ryuk e CryptoLocker

A repositório a seguir representa um código e resultados do mesmo. O mesmo se retrata da pesquisa sobre detecção de ransonwares, tendo seu início a pesquisa a cerca das caracteríticas do ransonware WannaCry, Ryuk e CryptoLocker. Este trabalho tem por objetivo identificar as features representativas para detecção dos ransomwares citados anteriormente. Para tanto, a ferramenta Cuckoo Sandbox é usada para capturar o comportamento de arquivos binários sem código malicioso e dos ransomwares. A partir disso, tal comportamento foi registrado através da geração de um dataset. Os resultados obtidos através do algoritmo de seleção de features Information Gain (IG) revelam quais são as 20 features mais relevantes dentre 170 features para detecção do malware estudado.

O fluxo de execução do código acima é o seguinte:

1. Arquivo de JSON amostra de cada binário é gerado pelo [Cuckoo Sandbox](https://cuckoosandbox.org).
2. Inicialização da função main e chamada da função captura_coluna 'Função criada para capturar todas as features para a filtragem do mesmo'.
```py 
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
```
3. Função json_arq 'Função criada para ler os arquivos JSON de um determinado diretório e realizar o tratamento dos dados para a criação de uma tabela informativa'
  ```py
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

  ```

## Começando 

A Figura ilustra o cenário de experimentação, que envolve o upload de binários (binary.exe) na ferramenta e a criação de máquinas virtuais por meio do software VirtualBox. A ferramenta possui um agente, criado em Python, que monitora e captura todo o conteúdo e mudanças realizas pelo binário durante sua execução. A ferramenta em questão é instalada em um computador Dell Inspiron 15 3000 com sistema operacional Ubuntu 18.04.

![image](https://user-images.githubusercontent.com/51774020/221394708-6ffee3aa-9d7e-4e2e-b6f9-cd51c90c1936.png)

Por fim, foi utilizado o ambiente de desenvolvimento Jupyterlab com a linguagem Python para processar o relatório resultante da análise do Cuckoo. Tal relatório é gerado no formato JavaScript Object Notation (JSON). A partir desse arquivo, foram selecionadas 170 features, tais como chamadas de sistemas e operações realizadas por cada binário executado. Dessa forma, foi possível a construção de um dataset com amostras maliciosas e legítimas (aplicações típicas de usuários comuns).
  
