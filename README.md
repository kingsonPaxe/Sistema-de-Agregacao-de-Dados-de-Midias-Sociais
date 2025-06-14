# Sistema de Agregação de Mídias Sociais
Este projeto é um sistema de agregação de mídias sociais desenvolvido em Python, projetado para coletar, armazenar e processar dados de plataformas como YouTube e Twitter. Com foco em eficiência e facilidade de uso, o sistema permite a análise centralizada de informações relevantes provenientes de diferentes redes sociais, facilitando a geração de insights e a visualização de dados para tomada de decisões.

- Coleta de dados via APIs do YouTube e Twitter
- Armazenamento eficiente dos dados utilizando MongoDB
- Processamento e manipulação de dados com bibliotecas Python.

## Tecnologias Utilizadas

- **Python**
- **Requests**: Para realizar requisições HTTP às APIs
- **Pymongo**: Para integração com o banco de dados MongoDB
- **Time & Datetime**: Para manipulação de datas e horários
- **MongoDB**: Banco de dados NoSQL para armazenamento dos dados coletados

## Como Executar

1. Clone este repositório.
2. Instale as dependências:
    ```bash
    pip install requests pymongo
    ```
3. Configure as credenciais das APIs do YouTube e Twitter.
4. Execute o script principal:
    ```bash
    python main.py
    ```

## Estrutura do Projeto

```
.
├── main.py
├── requirements.txt
└── README.md
```

## Observações

- Certifique-se de que o MongoDB está em execução antes de iniciar o sistema.
- As credenciais das APIs devem ser mantidas em segurança.

## Licença

Este projeto está licenciado sob os termos da licença MIT.

Project by: Jeovani Paxe