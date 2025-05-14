import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- CONFIGURAÇÃO GERAL ---
st.set_page_config(
    page_title="Dashboard Realização Semanal - RECAP",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS PARA MODO ESCURO ---
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

# --- TÍTULO DO DASHBOARD ---
st.markdown("## Dashboard de Realização Semanal - RECAP")

# --- CAMINHO DO ARQUIVO ---
ARQUIVO = "historico_recap.xlsx"

# --- LEITURA E TRATAMENTO DOS DADOS ---
if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO, sheet_name="REALIZACAO SEMANAL")
    df.columns = df.columns.str.strip().str.upper()
    df["SEMANA"] = df["SEMANA"].astype(str)
    df = df.sort_values("SEMANA")

    ultimo = df.iloc[-1]
    semana = ultimo["SEMANA"]
    valor_atual = float(ultimo["REALIZAÇÃO  SEMANAL"]) * 100
    meta = float(ultimo["META"]) * 100

    if "% AMEAÇAS INDICADOR MÊS" in df.columns:
        df["AMEACA_MES"] = df["% AMEAÇAS INDICADOR MÊS"].astype(float) * 100
    else:
        df["AMEACA_MES"] = np.nan

    if "DESCRIÇÃO DA META" in ultimo and pd.notnull(ultimo["DESCRIÇÃO DA META"]):
        resumo = str(ultimo["DESCRIÇÃO DA META"]).strip()
    else:
        resumo = ""

    # --- LAYOUT EM COLUNAS ---
    col1, col2 = st.columns([2, 1])

    # --- GRÁFICO DE ÁREA COM PROJEÇÃO ---
    with col1:
        st.markdown("#### Histórico de Realização Semanal")

        fig, ax = plt.subplots(figsize=(8, 4), facecolor='#0e1117')

        semanas = df["SEMANA"].tolist()
        valores = df["REALIZAÇÃO  SEMANAL"].astype(float).mul(100).tolist()
        ameacas = df["AMEACA_MES"].tolist()

        acima_meta = [v if v >= meta else meta for v in valores]
        abaixo_meta = [v if v < meta else np.nan for v in valores]

        ax.fill_between(semanas, acima_meta, color="#1f77b4", alpha=0.5, label="Acima da Meta")
        ax.fill_between(semanas, abaixo_meta, color="red", alpha=0.4, label="Abaixo da Meta")
        ax.plot(semanas, valores, color="white", marker='o', linewidth=1)

        for i, proj in enumerate(ameacas):
            if not np.isnan(proj):
                ax.plot(semanas[i], proj, marker='o', color="orange", markersize=6, label="% Ameaça Mês" if i == 0 else "")

        ax.axhline(y=meta, color='white', linestyle='--', linewidth=1, label=f"Meta = {meta:.2f}%")

        ax.set_facecolor('#0e1117')
        ax.set_ylabel("% Realização", color='white', fontsize=10)
        ax.set_xlabel("Semana", color='white', fontsize=10)
        ax.tick_params(axis='x', colors='white', rotation=45, labelsize=8)
        ax.tick_params(axis='y', colors='white', labelsize=8)
        ax.set_ylim(bottom=70)

        ax.set_xticks(range(0, len(semanas), 3))
        ax.set_xticklabels([semanas[i] for i in range(0, len(semanas), 3)])

        ax.legend(facecolor='#0e1117', edgecolor='white', labelcolor='white', fontsize=8)
        ax.grid(True, linestyle=':', linewidth=0.5, color='gray')

        fig.tight_layout()
        st.pyplot(fig)

    # --- KPI + RESUMO ---
    with col2:
        st.markdown(f"####  Semana {semana}")

        if valor_atual >= meta:
            cor = "#1f77b4"
            emoji = "✅"
            texto = "Dentro da meta"
        else:
            cor = "red"
            emoji = "⚠️"
            texto = "Abaixo da meta"

        st.markdown(f"""
        <div style="background-color:#1e1e1e;padding:6px 10px;border-radius:10px;text-align:center">
            <h1 style="color:{cor};font-size:36px;margin:4px 0">{valor_atual:.2f}%</h1>
            <p style="color:gray;font-size:13px;margin:2px 0">Realização Semanal</p>
            <p style="color:{cor};font-size:16px;margin:4px 0">{emoji} {texto}</p>
            <p style="color:white;font-size:11px;margin:2px 0">Meta: {meta:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)

        if resumo:
            st.markdown(f"""
            <div style="background-color:#2a2a2a;padding:8px 12px;margin-top:8px;border-radius:8px;">
                <p style="color:white;font-size:13px;margin:0;text-align:justify">📌 <b>Resumo:</b> {resumo}</p>
            </div>
            """, unsafe_allow_html=True)

else:
    st.error(f"❌ Arquivo '{ARQUIVO}' não encontrado.")
