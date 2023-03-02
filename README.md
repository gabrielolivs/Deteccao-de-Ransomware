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

![cuckoo drawio (2)](https://user-images.githubusercontent.com/51774020/222503136-20e0b5c2-c32f-42ee-bb48-5cfd0ae124e4.png)


Por fim, foi utilizado o ambiente de desenvolvimento Jupyterlab com a linguagem Python para processar o relatório resultante da análise do Cuckoo. Tal relatório é gerado no formato JavaScript Object Notation (JSON). A partir desse arquivo, foram selecionadas 170 features, tais como chamadas de sistemas e operações realizadas por cada binário executado. Dessa forma, foi possível a construção de um dataset com amostras maliciosas e legítimas (aplicações típicas de usuários comuns).

A fim de processar o relatório resultante da análise do Cuckoo, foi implementado um script na linguagem Python chamado script.py o qual é disponibilizado no repositório recém mencionado. Tal relatório, que é ilustrado na Figura, é gerado no formato JavaScript Object Notation (JSON). A partir desse arquivo, foram selecionadas 226 features para o WannaCry, 211 para o Ryuk e também 211 CryptoLock, tais como chamadas de sistemas e operações realizadas por cada binário executado. Dessa forma, foi possível a construção de 3 datasets com amostras maliciosas (WannaCry,Ryuk,CryptoLocker) e legítimas (aplicações típicas de usuários comuns). É importante destacar que cada dataset gerado contem amostras relativas aos 35 binários legítimos e 1 binário malicioso. Portanto, o que muda de um dataset para outro são as amostras do binário malicioso. Ou seja, cada dataset possui amostras de somente um dos binários maliciosos, além de amostras relativas ao 35 binários legítimos, que são as mesmas para cada base de dados. 

## Pré-requisitos

Para executar o script criado, é recomendado a instalação do software [Anaconda](https://www.anaconda.com/products/distribution) e que a máquina cujo a qual esteja utilizando, tenha pelo menos 8GB de memória RAM.

## Configuracao
Pimeiro, é necessário baixar todo o repositório em sua máquina. 

Siga os passos apresentados abaixo:

1 - No Windows, entraremos no repositorio em questao, va em '<> code' e baixe o ZIP:
![githubcerto1](https://user-images.githubusercontent.com/51774020/222516384-c7829379-c5a8-4367-b400-dee54f5e7976.gif)

2 - No local que desejar, extrairemos todos os arquivos.
![image](https://user-images.githubusercontent.com/51774020/222519289-ab2eb524-e8a6-430f-a43a-77a1b9767e79.png)

Ao executar o software recomendado, iremos utilizar o JupyterLab para realizar a execução e visualização de nossas features. (Imagem ilustrada abaixo)
![githubgif](https://user-images.githubusercontent.com/51774020/222509797-9426c199-a253-4c82-8728-6cc57d2db0bb.gif)

![githubcerto3](https://user-images.githubusercontent.com/51774020/222519569-24796901-5d5a-442a-84b0-c05e6dc06264.gif)

Agora, e necessario o dowload dos relatorios referente aos binarios nao maliciosos, o mesmo esta disponivel na url abaixo. O GitHub possui um limitador de tamanho de cada arquivo, portanto, foi incluido no Google Drive:

[Clique aqui](https://drive.google.com/drive/folders/1LcO4pn-Op9xZvBIw7NUQFFybP99dZ58B?usp=share_link) e baixe os reports.
![githubcerto4](https://user-images.githubusercontent.com/51774020/222520921-9c5a89bd-36e7-454d-8b66-b25ec0f21215.gif)

![image](https://user-images.githubusercontent.com/51774020/222522272-6ad38570-3650-419b-889c-411bff79a8bd.png)

## Executando

No JupyterLab, iremos dar inicio na execucao do stript em questao. na funcao 'main()' e necessario que o leitor insira o local do arquivo na pasta onde estao os arquivos JSON.

![image](https://user-images.githubusercontent.com/51774020/222523108-1651262c-6f2a-4909-839e-e5d1b59b0734.png)

Mude tambem, o nome cujo qual sera o nome do arquivo referente CSV

![image](https://user-images.githubusercontent.com/51774020/222524473-0061e80d-c54d-4006-9a76-87875eb9baa7.png)

Logo apos toda a configuracao, esta na hora de rodar. Basta pressionar CTRL+ENTER. O código estrara em seu funcionamento, e logo em seguida sera criado dois arquivos de resultado:

![image](https://user-images.githubusercontent.com/51774020/222534243-355ba71c-1c59-4e4b-8046-953440fbbfe5.png)

## Binarios

Os malware podem ser encontrados através da plataforma do [VirusShare](https://virusshare.com)

1. WannaCry             - 84c82835a5d21bbcf75a61706d8ab549
2. CryptoLocker         - c359a944d8c482b0bed83996cef3d2ca
3. Ryuk                 - f62bb82db62dd6b80908dcd79ea51fb2



