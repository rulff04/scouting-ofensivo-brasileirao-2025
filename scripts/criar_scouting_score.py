import pandas as pd
import numpy as np

arquivo = "base_scouting_2025.xlsx"
df = pd.read_excel(arquivo)

# =========================
# Garantir colunas numéricas
# =========================
colunas_numericas = [
    "90s",
    "Gols",
    "Assistências",
    "Participações em Gols",
    "Gols sem Pênalti",
    "Gols por 90",
    "Assistências por 90",
    "Participações em Gols por 90",
    "Gols sem Pênalti por 90",
    "Participações sem Pênalti por 90",
    "Finalizações",
    "Finalizações no Alvo",
    "Finalizações no Alvo %",
    "Finalizações por 90",
    "Finalizações no Alvo por 90",
    "Gols por Finalização",
    "Gols por Finalização no Alvo",
    "Passes decisivos por 90",
    "Grandes chances criadas por 90",
    "Dribles certos por 90",
    "Acerto no drible %",
    "Ranking",
]

for col in colunas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# Classificação de perfil
# =========================
def classificar_perfil(row):
    pos = str(row.get("Posição", "")).strip()

    if "GK" in pos:
        return "Excluir"
    if pos.startswith("DF") and "FW" not in pos:
        return "Excluir"

    if "FW" in pos and "MF" in pos:
        return "Híbrido Ofensivo"
    if "FW" in pos:
        return "Atacante"

    # Para MF puro, tenta identificar se é ofensivo
    finaliz_90 = row.get("Finalizações por 90", np.nan)
    passes_90 = row.get("Passes decisivos por 90", np.nan)
    ast_90 = row.get("Assistências por 90", np.nan)

    if pos == "MF":
        if (
            (pd.notna(finaliz_90) and finaliz_90 >= 1.0)
            or (pd.notna(passes_90) and passes_90 >= 1.0)
            or (pd.notna(ast_90) and ast_90 >= 0.08)
        ):
            return "Meia Ofensivo"
        return "Excluir"

    return "Excluir"

df["Perfil"] = df.apply(classificar_perfil, axis=1)

# =========================
# Filtrar ofensivos
# =========================
df_of = df[df["Perfil"].isin(["Atacante", "Híbrido Ofensivo", "Meia Ofensivo"])].copy()

# Se quiser reforçar a amostra mínima
if "90s" in df_of.columns:
    df_of = df_of[df_of["90s"] >= 10].copy()

# =========================
# Exigir pelo menos alguma cobertura do SofaScore
# =========================
colunas_sofa = [
    "Passes decisivos por 90",
    "Dribles certos por 90",
    "Acerto no drible %",
]

colunas_sofa_existentes = [c for c in colunas_sofa if c in df_of.columns]

if colunas_sofa_existentes:
    df_score = df_of[df_of[colunas_sofa_existentes].notna().sum(axis=1) >= 2].copy()
else:
    df_score = df_of.copy()

# =========================
# Função de percentil
# =========================
def percentil(coluna):
    return coluna.rank(pct=True)

# =========================
# Criar percentis das métricas
# =========================
metricas_percentil = {
    "pct_npg90": "Gols sem Pênalti por 90",
    "pct_ast90": "Assistências por 90",
    "pct_ga_npk90": "Participações sem Pênalti por 90",
    "pct_sot90": "Finalizações no Alvo por 90",
    "pct_g_sh": "Gols por Finalização",
    "pct_g_sot": "Gols por Finalização no Alvo",
    "pct_key90": "Passes decisivos por 90",
    "pct_big90": "Grandes chances criadas por 90",
    "pct_drib90": "Dribles certos por 90",
    "pct_dribpct": "Acerto no drible %",
}

for nova_col, col_original in metricas_percentil.items():
    if col_original in df_score.columns:
        df_score[nova_col] = percentil(df_score[col_original])

# =========================
# Subscores
# =========================
def media_disponivel(df_local, cols):
    cols_existentes = [c for c in cols if c in df_local.columns]
    if not cols_existentes:
        return np.nan
    return df_local[cols_existentes].mean(axis=1, skipna=True)

# Finalização
df_score["Subscore_Finalizacao"] = media_disponivel(
    df_score,
    ["pct_npg90", "pct_sot90", "pct_g_sh", "pct_g_sot"]
)

# Criação
df_score["Subscore_Criacao"] = media_disponivel(
    df_score,
    ["pct_ast90", "pct_key90", "pct_big90"]
)

# 1x1 / progressão
df_score["Subscore_Drible"] = media_disponivel(
    df_score,
    ["pct_drib90", "pct_dribpct"]
)

# Impacto ofensivo geral
df_score["Subscore_Impacto"] = media_disponivel(
    df_score,
    ["pct_ga_npk90"]
)

# =========================
# Score final com pesos
# =========================
df_score["Scouting Score"] = (
    df_score["Subscore_Finalizacao"] * 0.40
    + df_score["Subscore_Criacao"] * 0.30
    + df_score["Subscore_Drible"] * 0.15
    + df_score["Subscore_Impacto"] * 0.15
) * 100

df_score["Scouting Score"] = df_score["Scouting Score"].round(2)

# Ranking final
df_score = df_score.sort_values("Scouting Score", ascending=False).copy()
df_score["Ranking Scouting"] = range(1, len(df_score) + 1)

# =========================
# Seleção de colunas finais
# =========================
colunas_saida = [
    "Ranking Scouting",
    "Jogador",
    "Clube",
    "Posição",
    "Perfil",
    "Idade",
    "90s",
    "Gols",
    "Assistências",
    "Gols sem Pênalti por 90",
    "Assistências por 90",
    "Participações sem Pênalti por 90",
    "Finalizações por 90",
    "Finalizações no Alvo por 90",
    "Gols por Finalização",
    "Gols por Finalização no Alvo",
    "Passes decisivos por 90",
    "Grandes chances criadas por 90",
    "Dribles certos por 90",
    "Acerto no drible %",
    "Subscore_Finalizacao",
    "Subscore_Criacao",
    "Subscore_Drible",
    "Subscore_Impacto",
    "Scouting Score",
]

colunas_saida_existentes = [c for c in colunas_saida if c in df_score.columns]
df_score_final = df_score[colunas_saida_existentes].copy()

# =========================
# Salvar arquivos
# =========================
df_of.to_excel("base_ofensivos_2025.xlsx", index=False)
df_score_final.to_excel("scouting_score_2025.xlsx", index=False)

print("Arquivo salvo: base_ofensivos_2025.xlsx")
print("Arquivo salvo: scouting_score_2025.xlsx")
print(f"Total de ofensivos filtrados: {len(df_of)}")
print(f"Total de jogadores com score: {len(df_score_final)}")
print("\nTop 10 do Scouting Score:")
print(df_score_final.head(10))
