import re
import pandas as pd

arquivo_txt = "sofascore_complemento.txt"

with open(arquivo_txt, "r", encoding="utf-8") as f:
    linhas = [linha.strip() for linha in f if linha.strip()]

padrao = re.compile(
    r"^(?P<jogador>.+?)\s+"
    r"(?P<passes>\d+(?:\.\d+)?)\s+"
    r"(?P<grandes>\d+(?:\.\d+)?)\s+"
    r"(?P<dribles>\d+(?:\.\d+)?)\s+"
    r"(?P<acerto>\d+(?:\.\d+)?)$"
)

dados = []
i = 0

while i < len(linhas) - 2:
    ranking_linha = linhas[i]
    clube_linha = linhas[i + 1]
    jogador_linha = linhas[i + 2]

    if ranking_linha.isdigit():
        m = padrao.match(jogador_linha)
        if m:
            dados.append({
                "Ranking": int(ranking_linha),
                "Clube": clube_linha,
                "Jogador": m.group("jogador"),
                "Passes decisivos por 90": float(m.group("passes")),
                "Grandes chances criadas por 90": float(m.group("grandes")),
                "Dribles certos por 90": float(m.group("dribles")),
                "Acerto no drible %": float(m.group("acerto")),
            })
            i += 3
            continue

    i += 1

df = pd.DataFrame(dados)

arquivo_saida = "sofascore_complemento_2025.xlsx"
df.to_excel(arquivo_saida, index=False)

print(f"Arquivo salvo com sucesso: {arquivo_saida}")
print(df.head())
print(f"\nTotal de jogadores extraídos: {len(df)}")