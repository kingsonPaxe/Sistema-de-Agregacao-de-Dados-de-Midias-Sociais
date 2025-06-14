# Autor: Jeovani Paxe
# GitHub: kingsonPaxe

from main import *

# Cria uma instância da classe sad, responsável pelas operações de extração, transformação e carga de dados
sad_ = sad()
try:
    # Loop infinito
    while True:
        print("=============================================================== Sistema de agregação de dados ========================================================================")
        print("O que vamos coletar hoje?")
        escolher = input("[1] - Dados do Twitter?\n[2] - Dados do Youtube?\n   >>> ")

        # Se o usuário escolher a opção 1 então vai fazer o ETL dos dados do Twiter
        if int(escolher) == 1:
            pesquisar = input("Sobre o quê você quer pesquisar? \n   >> ")

            # Fazendo a Coleta
            numero_resultado = int(input(f"Digite o número de resultado você quer sobre '{pesquisar}': "))
            extrair_Twter = sad_.extractData_twitter(pesquisar, numero_resultado)
            print('\n================================================================== Extraindo dados =================================================== \n ',extrair_Twter)
            print(f"\n{datetime.now()} Dados coletados!") # O tempo em que a coleta foi feita

             # Transformação
            dados_transformados = sad_.transformData_twitter(extrair_Twter)
            print('\n================================================================================= Dados Transformados =============================================================== \n', dados_transformados)
            print(f"\n{datetime.now()} Dados trasnformados!") # O tempo em que a transformação foi feita
            
            load = sad_.load_dataTwitter(dados_transformados)
            print('\n================================================================================= Salvando os dados =============================================================== \n', load)
            print(f"{datetime.now()} Dados salvos!")# O tempo em que os dados foram salvos

        # Se o usuários escolher a opção 2 vai fazer o ETL dados do Youtube
        if int(escolher) == 2:
            pesquisar = input("Sobre o quê você quer pesquisar? \n   >> ")
            numero_resultado = int(input(f"Digite o número de resultado você quer sobre '{pesquisar}': "))

            # Fazendo a Coleta
            extrair_yb = sad_.extractData_youtube(pesquisar, numero_resultado)
            print('\n================================================================================= Extraindo dados ================================================================== \n ',extrair_yb)
            print(f"\n{datetime.now()} Dados coletados!") # Mostrar o tempo que foi feita a coleta
            
            # Transformação
            transf = sad_.transformData_youtube(extrair_yb)
            print('\n================================================================================= Dados Transformados =============================================================== \n', transf)
            print(f"\n{datetime.now()} Dados trasnformados!")

            # Carregamento
            load = sad_.loadData_youtube(transf)
            print('\n================================================================================= Salvando os dados =============================================================== \n', load)
            print(f"{datetime.now()} Dados salvos!")
        
        
        op2 = input("Deseja continuar [N/Y]?\n >> ")
        # Verifica se a opção é válida
        #Condição no caso do usúário desejar continuar com a execução do programa ou não
        if op2 == "N" or op2 == "n":
            print("================================================================ Fim do Programa ================================================================")
            break
        elif op2 == "Y" or op2 == "y":
            pass

except KeyboardInterrupt: # No caso do usuário querer para o programa é só clicar em ctrl+c para parar o programa 
    print("\n\033[31m Programa parado pelo usuário! \033[0m")
    print("============================================================================ Fim do Programa ============================================================================")
except Exception as erro: # Caso haja um erro numa linha...
        print(f"Erro durante a execução: \033[31m{erro}\033[0m") # Mostra essa informação