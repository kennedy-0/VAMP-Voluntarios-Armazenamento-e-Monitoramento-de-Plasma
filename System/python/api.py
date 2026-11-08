import json
import os
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE = os.path.dirname(os.path.abspath(__file__))


def raiz_projeto():
    """Sobe as pastas até achar o venv (pyvenv.cfg); a raiz é a pasta que contém o venv.
    Se o api.py não estiver dentro de um venv, usa a pasta acima dele."""
    pasta = BASE
    while pasta != os.path.dirname(pasta):
        if os.path.exists(os.path.join(pasta, "pyvenv.cfg")):
            return os.path.dirname(pasta)
        pasta = os.path.dirname(pasta)
    return os.path.dirname(BASE)


RAIZ = raiz_projeto()
NOMES_PASTA = ["", "dados", "DataBase", "database", "Database"]
# Procura ao lado do api.py, na pasta acima dele e na raiz do projeto
PASTAS = [os.path.join(base, p) for base in (BASE, os.path.dirname(BASE), RAIZ) for p in NOMES_PASTA]
# Pastas que não valem a pena varrer
IGNORAR = {"lib", "lib64", "site-packages", ".git", "node_modules", "__pycache__", "bin", "include"}

TABELAS = """
CREATE TABLE IF NOT EXISTS hemocentros (
    id INTEGER PRIMARY KEY, nome TEXT NOT NULL, cidade TEXT NOT NULL, estado TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS tipos_sanguineos (
    id INTEGER PRIMARY KEY, tipo TEXT NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS doadores (
    id INTEGER PRIMARY KEY, nome TEXT NOT NULL, email TEXT, telefone TEXT,
    possui_doenca TEXT NOT NULL DEFAULT 'NAO' CHECK (possui_doenca IN ('SIM','NAO')),
    doenca TEXT, tipo_sanguineo TEXT);
CREATE TABLE IF NOT EXISTS doacoes (
    id INTEGER PRIMARY KEY, doador_id INTEGER, hemocentro_id INTEGER, tipo_id INTEGER,
    data DATE, quantidade_ml INTEGER,
    FOREIGN KEY (doador_id) REFERENCES doadores(id),
    FOREIGN KEY (hemocentro_id) REFERENCES hemocentros(id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_sanguineos(id));
CREATE TABLE IF NOT EXISTS estoque (
    id INTEGER PRIMARY KEY, hemocentro_id INTEGER, tipo_id INTEGER,
    quantidade INTEGER NOT NULL, validade DATE,
    FOREIGN KEY (hemocentro_id) REFERENCES hemocentros(id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_sanguineos(id));
"""


def achar(nome):
    """Procura um arquivo pelo nome: primeiro nas pastas conhecidas,
    depois varrendo o projeto (a raiz do projeto)."""
    for pasta in PASTAS:
        caminho = os.path.abspath(os.path.join(pasta, nome))
        if os.path.exists(caminho):
            return caminho
    for raiz in (RAIZ, os.path.dirname(BASE)):
        for atual, subpastas, arquivos in os.walk(os.path.abspath(raiz)):
            subpastas[:] = [d for d in subpastas if d not in IGNORAR]
            if nome in arquivos:
                return os.path.join(atual, nome)
    return None


def banco_tem_dados(caminho):
    """True se o banco existe e já tem doações."""
    try:
        con = sqlite3.connect(caminho)
        n = con.execute("SELECT COUNT(*) FROM doacoes").fetchone()[0]
        con.close()
        return n > 0
    except sqlite3.Error:
        return False


def criar_banco_do_json(json_path, db_path):
    """Cria o vamp.db a partir do banco_de_dados_VAMP.json."""
    dados = json.load(open(json_path, encoding="utf-8"))
    con = sqlite3.connect(db_path)
    # Apaga tabelas antigas (ex.: criadas vazias pela versão anterior do api.py)
    for t in ("doacoes", "estoque", "doadores", "tipos_sanguineos", "hemocentros"):
        con.execute(f"DROP TABLE IF EXISTS {t}")
    con.executescript(TABELAS)
    for tabela, linhas in dados.items():
        if not linhas:
            continue
        colunas = list(linhas[0].keys())
        con.executemany(
            f"INSERT OR REPLACE INTO {tabela} ({','.join(colunas)}) "
            f"VALUES ({','.join('?' * len(colunas))})",
            [tuple(l[c] for c in colunas) for l in linhas])
    con.commit()
    con.close()
    print("Banco VAMP criado a partir do JSON:", db_path)


def preparar_banco():
    """Usa o vamp.db se tiver dados; senão, cria um a partir do JSON."""
    db = achar("vamp.db")
    if db and banco_tem_dados(db):
        return db
    js = achar("banco_de_dados_VAMP.json")
    if js is None:
        raise FileNotFoundError(
            "Não achei vamp.db com dados nem banco_de_dados_VAMP.json. "
            "Coloque um deles em ~/VAMP/dados/")
    destino = db or os.path.join(os.path.dirname(js), "vamp.db")
    criar_banco_do_json(js, destino)
    return destino


DB = preparar_banco()


def consultar(sql):
    """Executa um SELECT e devolve lista de dicionários."""
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    linhas = [dict(r) for r in con.execute(sql).fetchall()]
    con.close()
    return linhas


@app.route("/")
def home():
    # teste para ver se a API está OK
    return jsonify(msg="API ok")


@app.route("/api/doacoes")
def doacoes():
    # Uma linha por doação, já com cidade e tipo sanguíneo.
    # Os filtros (ano, cidade, tipo) são aplicados no navegador.
    return jsonify(consultar("""
        SELECT d.id, d.data, d.quantidade_ml,
               h.cidade, h.nome AS hemocentro,
               t.tipo
        FROM doacoes d
        JOIN hemocentros h ON h.id = d.hemocentro_id
        JOIN tipos_sanguineos t ON t.id = d.tipo_id
    """))


@app.route("/api/estoque")
def estoque():
    # Estoque atual por hemocentro e tipo sanguíneo.
    return jsonify(consultar("""
        SELECT e.quantidade, e.validade, h.cidade, t.tipo
        FROM estoque e
        JOIN hemocentros h ON h.id = e.hemocentro_id
        JOIN tipos_sanguineos t ON t.id = e.tipo_id
    """))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
