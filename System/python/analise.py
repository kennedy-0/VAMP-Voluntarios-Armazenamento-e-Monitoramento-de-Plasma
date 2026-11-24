# Exploração inicial dos dados do VAMP (Fase 01 - Descoberta)
# Lê o JSON original, confere a qualidade e mostra os primeiros achados.
import json
import sqlite3
from collections import Counter

dados = json.load(open("../dados/banco_de_dados_VAMP.json", encoding="utf-8"))

print("== Tabelas e quantidade de registros ==")
for tabela, linhas in dados.items():
    print(f"{tabela}: {len(linhas)}")

con = sqlite3.connect("../dados/vamp.db")

print("\n== Período coberto pelas doações ==")
print(con.execute("SELECT MIN(data), MAX(data) FROM doacoes").fetchone())

print("\n== Doações por tipo sanguíneo x estoque atual ==")
for linha in con.execute("""
    SELECT t.tipo,
           (SELECT COUNT(*) FROM doacoes d WHERE d.tipo_id = t.id) AS doacoes,
           (SELECT SUM(quantidade) FROM estoque e WHERE e.tipo_id = t.id) AS estoque
    FROM tipos_sanguineos t ORDER BY doacoes DESC"""):
    print(linha)

print("\n== Problemas de qualidade ==")
print("Doações sem doador cadastrado:", con.execute(
    "SELECT COUNT(*) FROM doacoes WHERE doador_id NOT IN (SELECT id FROM doadores)").fetchone()[0])
print("Doadores com doença:", Counter(r[0] for r in con.execute("SELECT possui_doenca FROM doadores")))
print("Atenção: e-mails são do tipo doadorN@exemplo.com -> dados sintéticos.")
