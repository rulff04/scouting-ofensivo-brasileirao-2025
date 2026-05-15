import pandas as pd
from io import StringIO

arquivo_html = "fbref_standard_2025.html"

with open(arquivo_html, "r", encoding="utf-8") as f:
    html = f.read()

# FBref costuma esconder tabelas dentro de comentários HTML
html = html.replace("<!--", "").replace("-->", "")

# Lê a tabela padrão de jogadores
df = pd.read_html(StringIO(html), attrs={"id": "stats_standard"})[0]

# Achata cabeçalhos multinível
if isinstance(df.columns, pd.MultiIndex):
    colunas_novas = []
    for a, b in df.columns:
        a = str(a).strip()
        b = str(b).strip()

        if "Unnamed" in a:
            nome = b
        elif a == "Playing Time" and b == "90s":
            nome = "90s"
        elif a == "Per 90 Minutes":
            nome = f"Per90_{b}"
        else:
            nome = b

        colunas_novas.append(nome)

    df.columns = colunas_novas

# Remove linha repetida de cabeçalho, se existir
if "Player" in df.columns:
    df = df[df["Player"] != "Player"].copy()

# Converte 90s para número
if "90s" in df.columns:
    df["90s"] = pd.to_numeric(df["90s"], errors="coerce")

# Filtra quem tem pelo menos 10 jogos completos equivalentes
if "90s" in df.columns:
    df = df[df["90s"] >= 10].copy()

# Mantém só as colunas que queremos
colunas_desejadas = [
    "Player",
    "Pos",
    "Squad",
    "Age",
    "90s",
    "Gls",
    "Ast",
    "G+A",
    "G-PK",
    "Per90_Gls",
    "Per90_Ast",
    "Per90_G+A",
    "Per90_G-PK",
    "Per90_G+A-PK",
]

colunas_existentes = [c for c in colunas_desejadas if c in df.columns]
df = df[colunas_existentes].copy()

# Renomeia para português
renomear = {
    "Player": "Jogador",
    "Pos": "Posição",
    "Squad": "Clube",
    "Age": "Idade",
    "90s": "90s",
    "Gls": "Gols",
    "Ast": "Assistências",
    "G+A": "Participações em Gols",
    "G-PK": "Gols sem Pênalti",
    "Per90_Gls": "Gols por 90",
    "Per90_Ast": "Assistências por 90",
    "Per90_G+A": "Participações em Gols por 90",
    "Per90_G-PK": "Gols sem Pênalti por 90",
    "Per90_G+A-PK": "Participações sem Pênalti por 90",
}

df.rename(columns=renomear, inplace=True)

arquivo_saida = "fbref_standard_2025.xlsx"
df.to_excel(arquivo_saida, index=False)

print(f"Arquivo salvo com sucesso: {arquivo_saida}")
print(df.head())