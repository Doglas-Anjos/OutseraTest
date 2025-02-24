# OutseraTest
Projeto destinado a criar uma api dos piores filmes do Golden Raspberry Awards

## Pre-Requisitos

- **Python:** 3.8.10  
- **pip:** 21.1.1  
- **Virtual Environment:** O projeto usa uma `venv` do python.

## Instalação
instruções para se preparar o ambiente necessário para rodar o servidor da API

1. **Clonar o repositório:**

```bash
git clone https://github.com/Doglas-Anjos/OutseraTest.git
cd OutseraTest
```

2. **Criar e Ativar Venv:**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Instalar as dependências**

```bash
pip install -r requirements.txt
```

## Configuração adicional
Adicione o arquivo `movielist.csv` no diretório principal do projeto clonado


## Rodando servidor Flask
Para startar o servidor Flask, execute:
```bash
python app.py
```
O server deverá subir no endereço http://127.0.0.1:5000 por padrão. Você pode acessar a API pelo browser.

## Rodando Testes de Integração
Testes de integração estão localizados na pasta `tests`, para rodar todas as integrações, execute:

```bash
python -m unittest discover -s tests
```

## Pre-Commit Hooks
O projeto usa pre-commit para assegurar que os testes são executados antes de fazer push. 
A configuração de pre-commit está em `.pre-commit-config.yaml`
para instalar os pre-commits hooks, execute:

```bash
pre-commit install --hook-type pre-push
```

## Informações Adicionais

- **Caching:** A API utiliza Flask-Caching para melhorar a performance, É possivel ajustar as configurações
em `app.py`

- **Estrutura do Projeto:**

````commandline
OutseraTest/
├── .git/
├── .pre-commit-config.yaml
├── app.py
├── LICENSE
├── defines.py
├── load_database.py
├── movielist.csv
├── requirements.txt
├── tests/
│   ├── __init__.py
│   └── FlaskIntegrationTest.py
└── README.md

````

## Endpoints

### `GET /producers`
Obtem o produtor com maior intervalo entre dois prêmios **Golden Raspberry Awards** consecutivos, e o que
obteve dois prêmios mais rápido


#### Retornos
- **200 OK**: Retorna o número aleatório gerado.
  ```json
    {
    "min": [
    {
    "producer": "Producer 1",
    "interval": 1,
    "previousWin": 2008,
    "followingWin": 2009
    },
    {
    "producer": "Producer 2",
    "interval": 1,
    "previousWin": 2018,
    "followingWin": 2019
    }
    ],
    "max": [
    {
    "producer": "Producer 1",
    "interval": 99,
    "previousWin": 1900,
    "followingWin": 1999
    },
    {
    "producer": "Producer 2",
    "interval": 99,
    "previousWin": 2000,
    "followingWin": 2099
    }
    ]
    }

- **500 Bad Request**: Se houver um problema interno no servidor ao se requisitar a API.
  ```json
    {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred on the server."
    }
  
- **404 Gone**: Qualquer outra url acessada que não está implementada, gerará um erro 404
  ```json
  {
    "error": "URL não encontrada!"
  }
