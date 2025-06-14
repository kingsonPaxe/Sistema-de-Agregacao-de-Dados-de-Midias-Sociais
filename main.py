# Autor: Jeovani Paxe
# GitHub: kingsonPaxe

# ============== Biblitecas usadas ==============
from time import sleep
import requests
import os 
from pymongo import MongoClient
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, time

#Fazendo a Conexão com MongoDB
client = MongoClient("mongodb://localhost:27017/")

load_dotenv()

# API keys
api_twitter = os.getenv('bear_token') # Token da API do twitter
apikey_youtube = os.getenv('Youtube_API_Key')


class sad:

    #Coletar dados do twiter
    def extractData_twitter(self, pesquisar_pub:str, max_results:int):
        self.search_pub = pesquisar_pub
        self.max_results = max_results

        # Fazendo a autenticação
        headers = { 
            'Authorization':f"Bearer {api_twitter}"
        }

        params = { # Selecionando alguns paramentros para a obtenção de dados
            "query": self.search_pub,
            "max_results": self.max_results,
            "tweet.fields": "created_at,public_metrics,author_id",
            "expansions": "author_id",
            "user.fields": "username,name"
        }
   
        url = "https://api.twitter.com/2/tweets/search/recent"
        self.response = requests.get(url, headers=headers, params=params) # Fazendo a requisição

        if self.max_results < 10 or self.max_results>100: # Não pode ser menor que 10 e maior que 100
            print(f"\033[31m Status Code: {self.response.status_code} \033[0m")
            print('\033[31m Att: o número de resultados tem que ser maior que 10 e menor que 100 \033[0m')

        elif self.response.status_code == 200: # Se a requisição for bem sucedida
            print(f"\033[32m Status Code: {self.response.status_code} \033[0m")
            return self.response.json()
        
        elif self.response.status_code == 429: # Limite de requisições atingido
            print("\033[31m Você atingiu o limite de requisições! Aguarde uns 15min. \033[0m")
            """ 
            fazendo o cálculo do tempo
            1 -----------------------------> 60s
                              X
            15 -----------------------------> x
            x = 60s * 15min/ 1min = 900/1 = 900s """

            sleep(900) # Equivalente a 15min, pois é o tempo limite para o fazer as requisições da API do Twitter
            return self.response.json()

        elif self.response.status_code == 401: # Erro de autenticação
            print("\033[31m Erro de autenticação! Verifique seu token de acesso. \033[0m")
            quit()
        elif self.response.status_code == 403: # Acesso negado
            # Acesso negado, pode ser que o token não tenha permissão para acessar o recurso
            print("\033[31m Acesso negado! Verifique suas permissões. \033[0m")
            quit() # Finaliza o programa
        # parra erro de internet
        elif self.response.status_code == 500: # Erro interno do servidor
            print("\033[31m Erro interno do servidor! Tente novamente mais tarde. \033[0m")
            quit()
        elif self.response.status_code == 503: # Serviço indisponível
            print("\033[31m Serviço indisponível! Tente novamente mais tarde. \033[0m")
            quit()
        else: # Outros erros
            print(f"\033[31m Status Code: {self.response.status_code}\033[0m")
            quit()

    # Fazendo a transformação
    def transformData_twitter(self, dados_json):
        self.dados_json = dados_json['data'] # Seleciona todos os valores que estão dentro da chave 'data'
        
        autores = dados_json['includes']['users'] 
        name = [autores['name'] for autores in autores]
        username = [autores['username'] for autores in autores]
        


        dados_transform = []
        show_index = 0
        for dados in self.dados_json: # Iterando sobre os dados

            # Pegando informaçãos importantes sobre os meus dados
            texto = dados['text']
            numero_retweets = dados['public_metrics']['retweet_count']
            numero_likes = dados['public_metrics']['like_count']
            criado_em = dados['created_at']
              
            # Adicionando todas essas infrmações em formato dicionário numa lista
            dados_transform.append(
                {
                    'Nome': name[show_index],
                    'Username': username[show_index],
                    'Texto': texto,
                    'Numero_Retweets': numero_retweets,
                    'Numero_likes': numero_likes,
                    'Data da criação': criado_em,
                    'ID_autor': dados['author_id']
                }
            )
            show_index+=1
        return dados_transform

    # Fazendo o carregamento no MongoDB
    def load_dataTwitter(self, dataTransform):
        db = client["Twitter"]
        pesq = self.search_pub.replace(" ", "_")
        colections = db[pesq]
        colections.insert_many(dataTransform)
        print(pd.DataFrame(dataTransform))
        return "Dados salvos com sucesso!"




    # Dados Youtube:
    # Estração
    def extractData_youtube(self, pesq_pub:str, max_result:int):
        self.pub = pesq_pub
        self.result = max_result
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part":"snippet",
            "q": self.pub,
            "type":"video",
            "maxResults":max_result,
            "key": apikey_youtube
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200: # Se a requisição for bem sucedida
            print(f"\033[32m Status Code: {response.status_code} \033[0m")
            return response.json()
        else:   # Se a requisição falhar
            print(f"\033[31m Status Code: {response.status_code}\033[0m")
            quit() # Finaliza o programa

    # Transformação dos dados do Youtube
    # Aqui eu vou transformar os dados que foram extraídos da API do Youtube
    def transformData_youtube(self, dados:dict):
        self.dados = dados
        dados_transform = []
        self.dados = self.dados['items']
        id_video = []#pegar as listas dos IDs

        # Extraindo dados do video e do id
        for show_data in self.dados: # Iterando sobre os dados
            # Pegando informaçãos importantes sobre os meus dados
            # Titulo, Canal, Data de publicação e ID do video
            # Aqui eu extraí o Titulo, Canal, Data de publicação e ID do video
            Titulo = show_data['snippet']['title']
            Canal = show_data['snippet']['channelTitle']
            Data = show_data['snippet']['publishedAt']
            vd_id = show_data['id']['videoId']
            id_video.append(vd_id)
            
            # Adicionando todas essas infrmações em formato dicionário numa lista
            dados_transform.append({
                "Titulo":Titulo,
                "Canal":Canal,
                "Data":Data
            })
        
        #  Através do  ID vou extrair os views, likes e comentarios
        stats = []
        
        # Fazendo a requisição para obter as estatísticas dos vídeos
        # Aqui eu peguei as estatísticas dos vídeos, como views, likes e comentários
        # A URL da API do Youtube para obter as estatísticas dos vídeos
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "statistics",
            "id": ",".join(id_video),
            "key": apikey_youtube
        }

        response = requests.get(url, params=params)
        info_videos = response.json()['items']

        for item in info_videos:
            vid = item['id']
            statistics = item['statistics']
            stats.append({
                "views": int(statistics.get("viewCount", 0)),
                "likes": int(statistics.get("likeCount", 0)),
                "comentarios": int(statistics.get("commentCount", 0)),
                "id": vid,
            })

        # unir os dois dicionarios[datatransform e stats] onde terá o Titulo, Canal, ID, likes, views, comentarios
        resultado = []
        index = 0
        for results in dados_transform:
            resultado.append({**dados_transform[index], **stats[index]})
            index+=1
        return resultado 
    
    # Guardando os dados no Mongo DB
    def loadData_youtube(self, data_transform:list):
        self.data_transform = data_transform
        db = client["Youtube"]# Criando o database

        pub = self.pub.replace(" ", "_")

        colecao = db[pub]# Criando a tabela
        colecao.insert_many(self.data_transform)
        print(pd.DataFrame(self.data_transform))
        return "Dados Salvo com Sucesso!"
         