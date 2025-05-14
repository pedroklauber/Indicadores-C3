import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- CONFIGURAÇÃO GERAL ---
st.set_page_config(
    page_title="Dashboard Vazamentos VC - RECAP",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- TÍTULO DO DASHBOARD ---
st.markdown("## Dashboard de Vazamentos VC - RECAP")

# --- CAMINHO DO ARQUIVO ---
ARQUIVO = "historico_recap.xlsx"

# --- LEITURA E TRATAMENTO DOS DADOS ---
if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO, sheet_name="VAZAMENTOS VC")
    df.columns = df.columns.str.strip().str.upper()
    df["DATA"] = pd.to_datetime(df["DATA"])
    df["SEMANA"] = df["SEMANA"].astype(str)
    df = df.sort_values("DATA")

    ultimo = df.iloc[-1]
    semana = ultimo["SEMANA"]
    vaz_atual = float(ultimo["VAZAMENTOS VP"])
    meta = float(ultimo["META"])

    if "DESCRIÇÃO DA META" in ultimo and pd.notnull(ultimo["DESCRIÇÃO DA META"]):
        resumo = str(ultimo["DESCRIÇÃO DA META"]).strip()
    else:
        resumo = ""

    # --- LAYOUT EM COLUNAS ---
    col1, col2 = st.columns([2, 1])

    # --- GRÁFICO DE ÁREA COLORIDA ---
    with col1:
        st.markdown("#### Histórico de Vazamentos VC")

        fig1, ax1 = plt.subplots(figsize=(8, 4), facecolor='white')

        semanas = df["SEMANA"].tolist()
        valores = df["VAZAMENTOS VP"].astype(float).tolist()

        abaixo_meta = [v if v <= meta else meta for v in valores]
        acima_meta = [v if v > meta else np.nan for v in valores]

        ax1.fill_between(semanas, abaixo_meta, color="#1f77b4", alpha=0.5, label="Abaixo da Meta")
        ax1.fill_between(semanas, acima_meta, color="red", alpha=0.3, label="Acima da Meta")
        ax1.plot(semanas, valores, color="#1f77b4", marker='o', linewidth=1)

        ax1.axhline(y=meta, color='gray', linestyle='--', label=f"Meta = {meta}")

        ax1.set_facecolor('white')
        ax1.set_ylabel("Qtd. Vazamentos", color='black', fontsize=10)
        ax1.set_xlabel("Semana", color='black', fontsize=10)
        ax1.tick_params(axis='x', colors='black', rotation=45, labelsize=8)
        ax1.tick_params(axis='y', colors='black', labelsize=8)

        ax1.set_xticks(range(0, len(semanas), 3))
        ax1.set_xticklabels([semanas[i] for i in range(0, len(semanas), 3)])

        ax1.legend(facecolor='white', edgecolor='black', labelcolor='black', fontsize=8)
        ax1.grid(True, linestyle=':', linewidth=0.5, color='lightgray')

        fig1.tight_layout()
        st.pyplot(fig1)

    # --- KPI + RESUMO ---
    with col2:
        st.markdown(f"####  Semana {semana}")

        if vaz_atual <= meta:
            cor = "green"
            emoji = "✅"
            texto = "Dentro da meta"
        else:
            cor = "red"
            emoji = "⚠️"
            texto = "Acima da meta"

        st.markdown(f"""
        <div style="background-color:#f5f5f5;padding:6px 10px;border-radius:10px;text-align:center">
            <h1 style="color:{cor};font-size:36px;margin:4px 0">{vaz_atual}</h1>
            <p style="color:#444;font-size:13px;margin:2px 0">Vazamentos na semana</p>
            <p style="color:{cor};font-size:16px;margin:4px 0">{emoji} {texto}</p>
            <p style="color:#333;font-size:11px;margin:2px 0">Meta: {meta} &nbsp; • &nbsp; Menos é Melhor</p>
        </div>
        """, unsafe_allow_html=True)

        if resumo:
            st.markdown(f"""
            <div style="background-color:#f0f0f0;padding:8px 12px;margin-top:8px;border-radius:8px;">
                <p style="color:#222;font-size:13px;margin:0;text-align:justify">📌 <b>Resumo:</b> {resumo}</p>
            </div>
            """, unsafe_allow_html=True)

else:
    st.error(f"❌ Arquivo '{ARQUIVO}' não encontrado.")
