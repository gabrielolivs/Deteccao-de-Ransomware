# Detecção de Ransomware: Um Estudo Acerca da Seleção de features da Camada de Aplicação

A repositório a seguir representa um código e resultados do mesmo. O mesmo se retrata da pesquisa sobre detecção de ransonwares, tendo seu início a pesquisa a cerca das caracteríticas do ransonware WannaCry. Este trabalho tem por objetivo identificar as features representativas para detecção do ransomware WannaCry. Para tanto, a ferramenta Cuckoo Sandbox é usada para capturar o comportamento de arquivos binários sem código malicioso e do WannaCry. A partir disso, tal comportamento foi registrado através da geração de um dataset. Os resultados obtidos através do algoritmo de seleção de features Information Gain (IG) revelam quais são as 20 features mais relevantes dentre 170 features para detecção do malware estudado.

O fluxo de execução do código acima é o seguinte:

1. Arquivo de JSON amostra de cada binário é gerado pelo [Cuckoo Sandbox](https://cuckoosandbox.org).
2. Inicialização da função main e chamada da função 'json_arq'.
3. Função json_arq 'Função criada para ler os arquivos JSON de um determinado diretório e realizar o tratamento dos dados para a criação de uma tabela informativa'
  ```py
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

                arquivo = open("teste2.txt","a")

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
                        
                    lines = open('teste2.txt','r').read().splitlines()
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
                    with open('teste2.txt','w') as arq:
                        arq.write('')
                    
                f.close()
                arquivo.close()
  
  ```

## Começando 

A Figura ilustra o cenário de experimentação, que envolve o upload de binários (binary.exe) na ferramenta e a criação de máquinas virtuais por meio do software VirtualBox. A ferramenta possui um agente, criado em Python, que monitora e captura todo o conteúdo e mudanças realizas pelo binário durante sua execução. A ferramenta em questão é instalada em um computador Dell Inspiron 15 3000 com sistema operacional Ubuntu 18.04.

![image](https://user-images.githubusercontent.com/51774020/221394708-6ffee3aa-9d7e-4e2e-b6f9-cd51c90c1936.png)

Por fim, foi utilizado o ambiente de desenvolvimento Jupyterlab com a linguagem Python para processar o relatório resultante da análise do Cuckoo. Tal relatório é gerado no formato JavaScript Object Notation (JSON). A partir desse arquivo, foram selecionadas 170 features, tais como chamadas de sistemas e operações realizadas por cada binário executado. Dessa forma, foi possível a construção de um dataset com amostras maliciosas (WannaCry) e legítimas (aplicações típicas de usuários comuns).
  
