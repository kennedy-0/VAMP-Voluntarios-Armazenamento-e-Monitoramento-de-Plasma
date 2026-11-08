# VAMP — Voluntários, Armazenamento e Monitoramento de Plasma

Sistema de gerenciamento e visualização de dados relacionados à doação de sangue, desenvolvido em Python, JavaScript, HTML e CSS.

## Sobre o projeto

O VAMP tem como objetivo organizar informações sobre doadores, hemocentros, doações e estoques de sangue, permitindo acompanhar os dados por meio de um painel interativo.

O sistema utiliza uma API para consultar os dados armazenados em um banco SQLite e apresentá-los em gráficos.

## Estrutura do projeto

```text
VAMP/
│
├── DataBase/
│   ├── vamp.db
│   └── banco_de_dados_VAMP.json
│
├── js/
│   └── main.js
│
├── python/
│   ├── api.py
│   └── analise.py
│
├── style/
│   └── style.css
│
└── index.html
```

## Tecnologias utilizadas

- **Python:** processamento e gerenciamento dos dados.
- **Flask:** desenvolvimento da API.
- **Flask-CORS:** comunicação entre frontend e backend.
- **SQLite:** armazenamento dos dados.
- **JavaScript:** filtros e atualização dos gráficos.
- **HTML5:** estrutura da interface.
- **CSS3:** estilização do painel.
- **Chart.js:** criação dos gráficos.

## Funcionalidades

- Consulta de doações realizadas.
- Monitoramento do estoque de bolsas de sangue.
- Visualização de doações por mês.
- Comparação de doações por cidade.
- Comparação por tipo sanguíneo.
- Filtros por ano, cidade e tipo sanguíneo.
- Indicadores de quantidade de doações e litros coletados.
- Análise exploratória e identificação de problemas nos dados.

## Banco de dados

O sistema utiliza SQLite para armazenar informações organizadas nas seguintes tabelas:

| Tabela | Descrição |
|---|---|
| hemocentros | Cadastro dos hemocentros |
| tipos_sanguineos | Tipos sanguíneos |
| doadores | Informações dos doadores |
| doacoes | Histórico de doações |
| estoque | Quantidade de bolsas disponíveis |

O arquivo JSON também pode ser utilizado como fonte para criação do banco SQLite.

## API

A API foi desenvolvida utilizando Flask e disponibiliza os seguintes endpoints:

| Rota | Descrição |
|---|---|
| `/` | Verifica se a API está funcionando |
| `/api/doacoes` | Retorna os registros de doações |
| `/api/estoque` | Retorna os dados do estoque |

A API utiliza a porta **5001**.

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
cd VAMP
```

Crie um ambiente virtual:

```bash
python3 -m venv venv
```

Ative o ambiente:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install flask flask-cors
```

## Executando o projeto

Inicie o backend:

```bash
python python/api.py
```

A API estará disponível em:

```text
http://localhost:5001
```

Depois, abra o arquivo `index.html` no navegador para visualizar o painel.

## Análise de dados

O arquivo `analise.py` realiza uma exploração inicial dos dados, apresentando:

- Quantidade de registros por tabela.
- Período abrangido pelas doações.
- Comparação entre doações e estoque por tipo sanguíneo.
- Verificação de doações sem doador cadastrado.
- Identificação de doadores com doenças registradas.

## Objetivo acadêmico

O VAMP é um projeto desenvolvido com o propósito de aplicar conhecimentos de programação, banco de dados, desenvolvimento web e análise de dados em uma solução voltada à organização de informações sobre doação de sangue.

---

**VAMP — Voluntários, Armazenamento e Monitoramento de Plasma.**
