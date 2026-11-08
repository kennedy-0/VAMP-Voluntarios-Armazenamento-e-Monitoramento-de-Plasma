# VAMP — Voluntários, Armazenamento e Monitoramento de Plasma

**Sistema de gerenciamento, monitoramento e análise de dados relacionados à doação de sangue.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-Backend-blue?logo=python" />
  <img src="https://img.shields.io/badge/JavaScript-Frontend-yellow?logo=javascript" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite" />
  <img src="https://img.shields.io/badge/Flask-API-black?logo=flask" />
</p>

---

## 1. Sobre o projeto

O **VAMP (Voluntários, Armazenamento e Monitoramento de Plasma)** é um projeto desenvolvido para organizar, consultar e analisar informações relacionadas à doação de sangue e ao gerenciamento de estoques em hemocentros.

A aplicação utiliza uma arquitetura separada entre frontend e backend. O backend é responsável pelo processamento das informações e comunicação com o banco de dados, enquanto o frontend apresenta os resultados por meio de indicadores, filtros e gráficos interativos.

O projeto também possui uma etapa de análise exploratória, destinada à identificação de padrões e possíveis inconsistências nos dados.

## 2. Objetivos

- Organizar informações sobre doadores e hemocentros.
- Registrar e consultar doações de sangue.
- Monitorar a disponibilidade de bolsas em estoque.
- Comparar informações por tipo sanguíneo.
- Facilitar a visualização dos dados por meio de gráficos.
- Aplicar conhecimentos de programação, banco de dados e análise de dados.

## 3. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Processamento e gerenciamento de dados |
| Flask | Desenvolvimento da API |
| Flask-CORS | Comunicação entre frontend e backend |
| SQLite | Armazenamento das informações |
| JavaScript | Lógica e interatividade do frontend |
| HTML5 | Estrutura da aplicação |
| CSS3 | Estilização da interface |
| Chart.js | Visualização gráfica dos dados |

## 4. Estrutura do projeto

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
├── index.html
│
└── README.md
```

### Responsabilidade de cada diretório

**DataBase/**
- `vamp.db`: banco de dados SQLite.
- `banco_de_dados_VAMP.json`: arquivo JSON utilizado como fonte de dados para a criação do banco.

**js/**
- `main.js`: comunicação com a API, aplicação de filtros e atualização dos gráficos.

**python/**
- `api.py`: gerenciamento do banco de dados e disponibilização dos endpoints.
- `analise.py`: exploração inicial e verificação da qualidade dos dados.

**style/**
- `style.css`: estilos e organização visual da interface.

**index.html**
- Estrutura principal do painel de monitoramento.

## 5. Funcionalidades

### Painel de monitoramento

O frontend permite visualizar informações consolidadas sobre as doações e o estoque.

Principais indicadores:

- Total de doações registradas.
- Quantidade total de sangue coletado em litros.
- Histórico de doações por mês.
- Distribuição de doações por cidade.
- Comparação entre doações e estoque por tipo sanguíneo.

### Sistema de filtros

A aplicação disponibiliza filtros interativos por:

- Ano.
- Cidade.
- Tipo sanguíneo.

Também possui uma opção para limpar os filtros e restaurar a visualização geral.

### Tipos sanguíneos

O sistema trabalha com os oito tipos sanguíneos:

- O-
- O+
- A-
- A+
- B-
- B+
- AB-
- AB+

## 6. Banco de dados

O VAMP utiliza SQLite para armazenar e relacionar as informações.

O banco possui cinco tabelas principais:

| Tabela | Descrição |
|---|---|
| `hemocentros` | Informações dos hemocentros, cidades e estados. |
| `tipos_sanguineos` | Cadastro dos tipos sanguíneos. |
| `doadores` | Informações cadastrais e indicadores de doenças. |
| `doacoes` | Histórico de doações, datas e quantidades coletadas. |
| `estoque` | Quantidade de bolsas disponíveis e respectivas validades. |

As tabelas utilizam identificadores e relacionamentos para conectar os registros.

### Inicialização automática do banco

O arquivo `api.py` possui uma rotina para localizar os arquivos necessários.

Seu funcionamento considera duas situações:

1. Quando encontra um `vamp.db` com registros de doações, utiliza o banco existente.
2. Quando não encontra um banco com dados, procura o arquivo JSON e utiliza suas informações para criar o banco SQLite.

**Atenção:** a rotina de criação atual remove as tabelas existentes antes de reconstruí-las. Portanto, mantenha uma cópia de segurança do banco antes de executar essa operação.

## 7. Backend e API

O backend utiliza Python e Flask para disponibilizar os dados ao frontend.

A API possui três rotas principais:

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verificação do funcionamento da API. |
| GET | `/api/doacoes` | Consulta as doações, cidades, hemocentros e tipos sanguíneos. |
| GET | `/api/estoque` | Consulta a quantidade de bolsas, validade, cidade e tipo sanguíneo. |

### Exemplo de resposta

Consulta de doações:

```json
[
  {
    "id": 1,
    "data": "2026-01-15",
    "quantidade_ml": 450,
    "cidade": "Recife",
    "hemocentro": "Hemocentro Central",
    "tipo": "O+"
  }
]
```

A resposta é convertida para JSON, permitindo que o JavaScript consuma os dados utilizando `fetch()`.

**Endereço padrão da API:**

```text
http://localhost:5001
```

## 8. Análise exploratória dos dados

O arquivo `analise.py` representa a primeira etapa de exploração dos dados do VAMP.

Essa etapa tem como objetivo conhecer a estrutura do banco, verificar a distribuição das informações e identificar possíveis problemas de qualidade.

### Fase 01 — Descoberta

As análises realizadas incluem:

**Quantidade de registros**
- Identificação das tabelas existentes no JSON.
- Contagem de registros por tabela.

**Período das doações**
- Identificação da primeira data registrada.
- Identificação da última data registrada.

**Distribuição por tipo sanguíneo**
- Contagem de doações por tipo.
- Comparação entre doações e estoque atual.

**Qualidade dos dados**
- Verificação de doações sem doador cadastrado.
- Contagem de doadores com e sem doenças registradas.
- Identificação de dados sintéticos utilizados nos testes.

### Bibliotecas utilizadas

- `json`: leitura dos dados.
- `sqlite3`: consultas ao banco.
- `collections.Counter`: contagem de ocorrências.

## 9. Instalação e configuração

### Pré-requisitos

- Python 3.
- Git.
- Navegador atualizado.

### Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd VAMP
```

### Criar ambiente virtual

```bash
python3 -m venv venv
```

### Ativar o ambiente virtual

Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Instalar dependências

```bash
pip install flask flask-cors
```

## 10. Executando a aplicação

### Iniciar o backend

A partir da raiz do projeto:

```bash
python python/api.py
```

A API será disponibilizada na porta 5001.

### Iniciar o frontend

Em outro terminal, na raiz do projeto:

```bash
python3 -m http.server 8000
```

Acesse no navegador:

```text
http://localhost:8000
```

A API e o frontend devem estar em execução simultaneamente.

**Observação:** o arquivo `main.js` utiliza `http://localhost:5001/api` como endereço padrão. Para acessar por outro dispositivo, altere esse endereço para o IP do computador que executa o backend.

## 11. Próximas melhorias

Algumas possibilidades de evolução do projeto:

- Implementação de cadastro e gerenciamento de doadores.
- Sistema de autenticação e controle de acesso.
- Cadastro e atualização de doações.
- Monitoramento de estoque em tempo real.
- Alertas para bolsas próximas do vencimento.
- Novos indicadores e relatórios estatísticos.
- Exportação de relatórios.
- Melhorias na validação e integridade dos dados.

## 12. Considerações finais

O VAMP busca demonstrar como ferramentas de desenvolvimento web, bancos de dados e análise de informações podem ser aplicadas na organização de dados relacionados à doação de sangue.

O projeto também representa uma oportunidade de desenvolver conhecimentos práticos em Python, JavaScript, SQL, integração entre sistemas e visualização de dados.

---

## Licença

Projeto desenvolvido para fins acadêmicos e de aprendizado.

## Autor

**Daniel Kennedy**

Desenvolvimento de software | Python | JavaScript | Linux | Banco de Dados

---

<p align="center">
  <strong>VAMP — Tecnologia aplicada à organização e ao monitoramento de doações de sangue.</strong>
</p>
