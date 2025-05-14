import streamlit as st
import pandas as pd
import numpy as np
import os

# --- CONFIGURAÇÃO GERAL ---
st.set_page_config(
    page_title="Dashboard Consolidado - KPIs",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.image("logo.png", width=150)
st.markdown("## Indicadores Consolidados")





# --- LOGO NO SIDEBAR ---
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <img src="logo.png" width="150">
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("### Relatório de Indicadores")
st.sidebar.markdown("Atualizado semanalmente com base no histórico.")

# --- CSS ESCURO ---
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #cfcfcf;
}
[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
}
[data-testid="stHeader"] {
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)

# --- CAMINHO DO ARQUIVO ---
ARQUIVO = "historico_recap.xlsx"

# --- FUNÇÃO DE EXTRAÇÃO SEGURA ---
def extrair_kpi(aba, campo_valor, campo_meta):
    df = pd.read_excel(ARQUIVO, sheet_name=aba)
    df.columns = df.columns.str.strip().str.upper()
    df = df.dropna(subset=[campo_valor, campo_meta])
    ultimo = df.iloc[-1]
    valor = float(ultimo[campo_valor])
    meta = float(ultimo[campo_meta])
    return valor, meta

# --- GRUPOS DE INDICADORES ---
grupos = {
    "Indicadores Contratuais": [
        {
            "nome": "Realização Semanal", "aba": "REALIZACAO SEMANAL",
            "campo_valor": "REALIZAÇÃO  SEMANAL", "campo_meta": "META",
            "tipo": "maior", "unidade": "%"
        },
        {
            "nome": "Tempo de Planejamento", "aba": "TEMPO DE PLANEJAMENTO",
            "campo_valor": "TEMPO DE PLANEJAMENTO", "campo_meta": "META",
            "tipo": "menor", "unidade": " dias"
        },
        {
            "nome": "Disp. Equipamentos", "aba": "DISP.EQUIPAMENTOS",
            "campo_valor": "DISPONIBILIDADE", "campo_meta": "META",
            "tipo": "maior", "unidade": "%"
        },
    ],
    "Indicadores Cliente": [
        {
            "nome": "IARI", "aba": "IARI", "campo_valor": "% INDICADOR ATUAL",
            "campo_meta": "META", "tipo": "maior", "unidade": "%"
        },
        {
            "nome": "IAZF", "aba": "IAZF", "campo_valor": "IMPACTO PREVISTO",
            "campo_meta": "META", "tipo": "maior", "unidade": "%"
        },
        {
            "nome": "PFCEO", "aba": "PFCEO", "campo_valor": "EQUIPAMENTOS NO PAINEL",
            "campo_meta": "META", "tipo": "menor", "unidade": ""
        },
        {
            "nome": "Vazamentos Totais", "aba": "VAZAMENTOS GERAL",
            "campo_valor": "VAZAMENTOS TOTAIS", "campo_meta": "META",
            "tipo": "menor", "unidade": ""
        },
        {
            "nome": "Vazamentos Vapor/Condens", "aba": "VAZAMENTOS VC",
            "campo_valor": "VAZAMENTOS VP", "campo_meta": "META",
            "tipo": "menor", "unidade": ""
        },
        {
            "nome": "Disp. Purgadores", "aba": "DISP.PURGADORES",
            "campo_valor": "IDP", "campo_meta": "META",
            "tipo": "maior", "unidade": "%"
        }
    ]
}

# --- GERAR DASHBOARD POR GRUPO ---
for titulo, indicadores in grupos.items():
    st.markdown(f"###  {titulo}")
    colunas = st.columns(3)

    for i, ind in enumerate(indicadores):
        with colunas[i % 3]:
            valor, meta = extrair_kpi(ind["aba"], ind["campo_valor"], ind["campo_meta"])
            tipo = ind["tipo"]
            unidade = ind.get("unidade", "")

            if unidade == "%" and valor > 1.5:
                valor = valor / 100
            if unidade == "%" and meta > 1.5:
                meta = meta / 100

            status_ok = valor >= meta if tipo == "maior" else valor <= meta
            cor = "#1f77b4" if status_ok else "red"
            emoji = "✅" if status_ok else "⚠️"
            status = "Dentro da meta" if status_ok else "Fora da meta"

            valor_formatado = f"{valor * 100:.2f}%" if unidade == "%" else f"{valor:.2f}{unidade}"
            meta_formatada = f"{meta * 100:.2f}%" if unidade == "%" else f"{meta:.2f}{unidade}"

            # Espaço extra para a linha inferior da seção "Indicadores Cliente"
            espaco_extra = ""
            if titulo == "Indicadores Cliente" and i in [3, 4, 5]:
                espaco_extra = "<div style='margin-top: 24px;'></div>"

            st.markdown(f"""{espaco_extra}<p style='font-size:14px; font-weight:bold'>{ind['nome']}</p>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background-color:#1e1e1e;padding:10px;border-radius:10px;text-align:center">
                <h1 style="color:{cor};font-size:32px;margin:4px 0">{valor_formatado}</h1>
                <p style="color:{cor};font-size:15px;margin:0">{emoji} {status}</p>
                <p style="color:white;font-size:11px;margin:0">Meta: {meta_formatada}</p>
            </div>
            """, unsafe_allow_html=True)

    if titulo == "Indicadores Contratuais":
        st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)
