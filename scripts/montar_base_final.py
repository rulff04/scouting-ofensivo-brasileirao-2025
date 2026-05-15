import pandas as pd
import unicodedata
import re

# =========================
# Funções auxiliares
# =========================
def normalizar_texto(texto):
    if pd.isna(texto):
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r"\s+", " ", texto)
    return texto

def normalizar_clube(clube):
    clube = normalizar_texto(clube)

    mapa = {
        "red bull bragantino": "bragantino",
        "rb bragantino": "bragantino",
        "botafogo": "botafogo (rj)",
        "atletico-mg": "atletico mineiro",
        "atletico mg": "atletico mineiro",
        "sao paulo fc": "sao paulo",
        "corinthians paulista": "corinthians",
        "sport": "sport recife",
    }

    return mapa.get(clube, clube)

# =========================
# Leitura dos arquivos
# =========================
df_standard = pd.read_excel("fbref_standard_2025.xlsx")
df_shooting = pd.read_excel("fbref_shooting_2025.xlsx")
df_sofa = pd.read_excel("sofascore_complemento_2025.xlsx")

# =========================
# Criação de chaves
# =========================
for df in [df_standard, df_shooting, df_sofa]:
    df["jogador_key"] = df["Jogador"].apply(normalizar_texto)
    df["clube_key"] = df["Clube"].apply(normalizar_clube)

# =========================
# Remove duplicatas por segurança
# =========================
df_standard = df_standard.drop_duplicates(subset=["jogador_key", "clube_key"])
df_shooting = df_shooting.drop_duplicates(subset=["jogador_key", "clube_key"])
df_sofa = df_sofa.drop_duplicates(subset=["jogador_key", "clube_key"])

# =========================
# Merge FBref Standard + Shooting
# =========================
colunas_shooting = [
    "jogador_key", "clube_key",
    "Finalizações",
    "Finalizações no Alvo",
    "Finalizações no Alvo %",
    "Finalizações por 90",
    "Finalizações no Alvo por 90",
    "Gols por Finalização",
    "Gols por Finalização no Alvo",
    "Pênaltis Convertidos",
    "Pênaltis Batidos",
]

colunas_shooting_existentes = [c for c in colunas_shooting if c in df_shooting.columns]
df_shooting = df_shooting[colunas_shooting_existentes].copy()

base = df_standard.merge(
    df_shooting,
    on=["jogador_key", "clube_key"],
    how="left"
)

# =========================
# Merge com SofaScore
# =========================
colunas_sofa = [
    "jogador_key", "clube_key",
    "Passes decisivos por 90",
    "Grandes chances criadas por 90",
    "Dribles certos por 90",
    "Acerto no drible %",
    "Ranking"
]

colunas_sofa_existentes = [c for c in colunas_sofa if c in df_sofa.columns]
df_sofa = df_sofa[colunas_sofa_existentes].copy()

base = base.merge(
    df_sofa,
    on=["jogador_key", "clube_key"],
    how="left"
)

# =========================
# Organiza colunas finais
# =========================
colunas_finais_preferidas = [
    "Jogador",
    "Clube",
    "Posição",
    "Idade",
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
    "Ranking"
]

colunas_finais = [c for c in colunas_finais_preferidas if c in base.columns]
base = base[colunas_finais].copy()

# =========================
# Diagnóstico: quem do SofaScore não casou
# =========================
comparacao = df_sofa.merge(
    df_standard[["jogador_key", "clube_key"]],
    on=["jogador_key", "clube_key"],
    how="left",
    indicator=True
)

sem_match = comparacao[comparacao["_merge"] == "left_only"].copy()

# Para deixar legível no arquivo de diagnóstico
if not sem_match.empty:
    diagnostico = df_sofa.merge(
        sem_match[["jogador_key", "clube_key"]],
        on=["jogador_key", "clube_key"],
        how="inner"
    )
else:
    diagnostico = pd.DataFrame()

# =========================
# Salva arquivos
# =========================
base.to_excel("base_scouting_2025.xlsx", index=False)

if not diagnostico.empty:
    diagnostico.to_excel("sofascore_sem_match.xlsx", index=False)

print("Arquivo principal salvo com sucesso: base_scouting_2025.xlsx")
print(f"Total de linhas na base final: {len(base)}")

if not diagnostico.empty:
    print(f"Jogadores do SofaScore sem correspondência no FBref: {len(diagnostico)}")
    print("Arquivo de diagnóstico salvo: sofascore_sem_match.xlsx")
else:
    print("Todos os jogadores do SofaScore casaram com a base do FBref.")