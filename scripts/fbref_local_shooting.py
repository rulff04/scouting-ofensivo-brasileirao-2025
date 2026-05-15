import pandas as pd
from io import StringIO

arquivo_html = "fbref_shooting_2025.html"

with open(arquivo_html, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("<!--", "").replace("-->", "")

df = pd.read_html(StringIO(html), attrs={"id": "stats_shooting"})[0]

if isinstance(df.columns, pd.MultiIndex):
    colunas_novas = []
    for a, b in df.columns:
        a = str(a).strip()
        b = str(b).strip()

        if "Unnamed" in a:
            nome = b
        elif a == "Standard" and b == "90s":
            nome = "90s"
        elif a == "Expected":
            nome = f"Expected_{b}"
        else:
            nome = b

        colunas_novas.append(nome)

    df.columns = colunas_novas

if "Player" in df.columns:
    df = df[df["Player"] != "Player"].copy()

if "90s" in df.columns:
    df["90s"] = pd.to_numeric(df["90s"], errors="coerce")
    df = df[df["90s"] >= 10].copy()

colunas_desejadas = [
    "Player",
    "Pos",
    "Squad",
    "90s",
    "Sh",
    "SoT",
    "SoT%",
    "Sh/90",
    "SoT/90",
    "G/Sh",
    "G/SoT",
    "PK",
    "PKatt",
]

colunas_existentes = [c for c in colunas_desejadas if c in df.columns]
df = df[colunas_existentes].copy()

renomear = {
    "Player": "Jogador",
    "Pos": "Posição",
    "Squad": "Clube",
    "90s": "90s",
    "Sh": "Finalizações",
    "SoT": "Finalizações no Alvo",
    "SoT%": "Finalizações no Alvo %",
    "Sh/90": "Finalizações por 90",
    "SoT/90": "Finalizações no Alvo por 90",
    "G/Sh": "Gols por Finalização",
    "G/SoT": "Gols por Finalização no Alvo",
    "PK": "Pênaltis Convertidos",
    "PKatt": "Pênaltis Batidos",
}

df.rename(columns=renomear, inplace=True)

arquivo_saida = "fbref_shooting_2025.xlsx"
df.to_excel(arquivo_saida, index=False)

print(f"Arquivo salvo com sucesso: {arquivo_saida}")
print(df.head())