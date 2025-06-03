import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import numpy as np

# --- CONFIGURAÇÃO GERAL ---
st.set_page_config(
    page_title="Dashboard Disp. Purgadores",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- TÍTULO DO DASHBOARD ---
st.image("logo.png", width=180)
st.markdown("## Dashboard - Disponibilidade de Purgadores")

# --- CAMINHO DO ARQUIVO ---
ARQUIVO = "historico_recap.xlsx"

# --- LEITURA E TRATAMENTO DOS DADOS ---
if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO, sheet_name="DISP.PURGADORES")
    df.columns = df.columns.str.strip().str.upper()
    df["DATA"] = pd.to_datetime(df["DATA"])
    df["MÊS"] = df["DATA"].dt.strftime("%Y-%m")
    df = df.sort_values("DATA")

    ultimo = df.iloc[-1]
    semana = ultimo["SEMANA"]
    valor_atual = float(ultimo["IDP"]) * 100
    meta = float(ultimo["META"]) * 100

    # --- LAYOUT EM COLUNAS ---
    col1, col2 = st.columns([2, 1])

    # --- GRÁFICO DE ÁREA COLORIDA ---
    with col1:
        st.markdown("#### Histórico de Disponibilidade")

        fig1, ax1 = plt.subplots(figsize=(10, 5), facecolor='white')

        meses = df["MÊS"].tolist()
        valores = (df["IDP"].astype(float) * 100).tolist()

        abaixo_meta = [v if v <= meta else meta for v in valores]
        acima_meta = [v if v > meta else np.nan for v in valores]

        ax1.fill_between(meses, abaixo_meta, color="#1f77b4", alpha=0.5, label="Abaixo da Meta")
        ax1.fill_between(meses, acima_meta, color="red", alpha=0.3, label="Acima da Meta")
        ax1.plot(meses, valores, color="#1f77b4", marker='o', linewidth=1)

        for i, v in enumerate(valores):
            ax1.text(meses[i], v + 1, f"{v:.1f}%", color='black', fontsize=8, ha='center')

        ax1.axhline(y=meta, color='gray', linestyle='--', label=f"Meta = {meta:.0f}%")

        ax1.set_facecolor('white')
        ax1.set_ylabel("Disponibilidade (%)", color='black', fontsize=10)
        ax1.set_xlabel("Mês", color='black', fontsize=10)
        ax1.tick_params(axis='x', colors='black', rotation=45, labelsize=8)
        ax1.tick_params(axis='y', colors='black', labelsize=8)

        ax1.set_ylim(bottom=70)
        ax1.set_xticks(range(len(meses)))
        ax1.set_xticklabels(meses)

        ax1.legend(facecolor='white', edgecolor='black', labelcolor='black', fontsize=8)
        ax1.grid(True, linestyle=':', linewidth=0.5, color='lightgray')

        fig1.tight_layout()
        st.pyplot(fig1)

    # --- KPI ---
    with col2:
        st.markdown(f"#### Semana {semana}")

        if valor_atual >= meta:
            cor = "green"
            emoji = "✅"
            texto = "Dentro da meta"
        else:
            cor = "red"
            emoji = "⚠️"
            texto = "Fora da meta"

        st.markdown(f"""
        <div style="background-color:#f5f5f5;padding:6px 10px;border-radius:10px;text-align:center">
            <h1 style="color:{cor};font-size:36px;margin:4px 0">{valor_atual:.2f}%</h1>
            <p style="color:#444;font-size:13px;margin:2px 0">Disponibilidade Atual</p>
            <p style="color:{cor};font-size:16px;margin:4px 0">{emoji} {texto}</p>
            <p style="color:#333;font-size:11px;margin:2px 0">Meta: {meta:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error(f"❌ Arquivo '{ARQUIVO}' não encontrado.")
