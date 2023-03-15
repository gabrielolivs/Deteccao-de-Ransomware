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

Os binários que foram executados, são binários que foram executados na ferramenta online do Cuckoo Sandbox e ferramentas populares, abaixo estaremos disponibilizando as hashes MD5 de cada binário não malicioso. A coleta dos binários foi realizada de duas formas, 15 dos mesmos foram retirados de binários comumente utilizados por usuários, como por exemplo (Google, Safari, Firefox, Opera, OperaGX e etc.), os demais binários foram coletados através da ferramenta [Cukoo Sandbox online](https://cuckoo.cert.ee/analysis/). Foi realizado uma coleta pelas análises de binários que possuem o scores mais baixos do mesmo e foi executado no Cuckoo Sandbox que foi intalado em nossa máquina, para evidenciar se o binário realmente não possui um score baixo e que não possue ações maliciosas. 

1.  232375fbdc2980ecd442d64ade1d5b3d
2.  5cce735d2c777c89e4cd11de55040891
3.  0bbcb8517d197ca042ec768c3f4566b3
4.  5c12cdf9b3313ef407151bfb22c883ef
5.  9fdca2eff2bac21d71a89d28518110bc
6.  ba736eea008423b9f1812157c311985a
7.  f9448ca2887ece5ca0c0e17f88e926a8
8.  7a0dfc5353ff6de7de0208a29fa2ffc9
9.  5790aabc5d5126ac5358324888275f54
10. fee11f37a9f3527f23f3b88ed6690a9a
11. 2f1d549c993a1360f241f8f119bb0e41
12. 8d26a0efa7369000827b3642eccf82af
13. f69d2d5185414faabcb5d4a07c78dea4
14. 42c383425dd636200dc1c0b30b3f7b14
15. a09e62520db5469a3dff49e8e3f2ac7c
16. 1af5d7d5a5e6efda0fd2cc763be8dd6f
17. e2d7e115c852f8d2f956afb600b51e7e
18. 13388b26b03e3384650a4ae0e3df37be
19. 31b3069cef380b4bf85e75a8885bcee8
20. 8a2ad04c5c1529183ee2e1a2245a0a8a
21. 0477dc80d3f44e28f0bccbb6b3d3d2a7
22. baca971eb8473ee7364db9c060fcde07
23. 411f46b0ffa685494f4149649b71550d
24. d5382d619115cf605dda008f532f867a
25. 382512660e69cb770579f0e16a94ed66
26. 56af723d25b24ac57452f8a66c59dab4
27. 68e6a5a62580ffa81e810f4e9feccf47
28. cb544cff55d55421cb615905e53ad45a
29. cc66e41c9e1317470a15ea229cc9e223
30. 91eed1131ead9f2b858ddab531bea037
31. 468f8b574c793e2d52af108f1a352d07
32. e2b8917b8544d1150c832d7563c76beb
33. 5ad27aff27dd768189be9c00c7e7a0af
34. 77db51e334b21c0c3cccbffaa73d8483
35. f415f70e9db33a21d1b7dfaf9a3fa31e



