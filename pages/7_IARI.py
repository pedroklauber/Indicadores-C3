import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- CONFIGURAÇÃO GERAL ---
st.set_page_config(
    page_title="Dashboard IARI - RECAP",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- TÍTULO DO DASHBOARD ---
st.markdown("## Dashboard de IARI - RECAP")

# --- CAMINHO DO ARQUIVO ---
ARQUIVO = "historico_recap.xlsx"

# --- LEITURA E TRATAMENTO DOS DADOS ---
if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO, sheet_name="IARI")
    df.columns = df.columns.str.strip().str.upper()
    df["DATA"] = pd.to_datetime(df["DATA"])
    df["SEMANA"] = df["SEMANA"].astype(str)
    df = df.sort_values("SEMANA")

    ultimo = df.iloc[-1]
    semana = ultimo["SEMANA"]
    valor_atual = float(ultimo["% INDICADOR ATUAL"]) * 100
    meta = float(ultimo["META"]) * 100

    if "% AMEÇAS INDICADOR MÊS" in df.columns:
        df["AMEACA_MES"] = df["% AMEÇAS INDICADOR MÊS"].astype(float) * 100
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
        st.markdown("#### Histórico do IARI")

        fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')

        semanas = df["SEMANA"].tolist()
        valores = df["% INDICADOR ATUAL"].astype(float).mul(100).tolist()
        ameacas = df["AMEACA_MES"].tolist()

        x = np.arange(len(semanas))
        largura = 0.6

        # Barras principais - IARI (azul)
        barras_iari = ax.bar(x, valores, width=largura, color="#1f77b4", label="% IARI Atual")

        # Barras de Ameaça (cinza claro), mais estreitas sobre as azuis
        for i, val in enumerate(ameacas):
            if not np.isnan(val):
                ax.bar(x[i], val, width=largura * 0.4, color="#a9a9a9", label="% Ameaça Mês" if i == 0 else "")

        # Rótulos nas barras de IARI
        for rect, val in zip(barras_iari, valores):
            ax.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.5, f"{val:.1f}%", 
                    ha='center', va='bottom', fontsize=7)

        # Rótulos nas barras de Ameaça
        for i, val in enumerate(ameacas):
            if not np.isnan(val):
                ax.text(x[i], val + 0.5, f"{val:.1f}%", ha='center', va='bottom', fontsize=7, color='black')

        # Linha da meta
        ax.axhline(y=meta, color='gray', linestyle='--', linewidth=1.2, label=f"Meta ({meta:.2f}%)")

        # Eixos e layout
        ax.set_facecolor('white')
        ax.set_ylabel("% IARI", fontsize=9, color='black')
        ax.set_xlabel("Semana", fontsize=9, color='black')
        ax.set_xticks(x)
        ax.set_xticklabels(semanas, rotation=45, ha='right', fontsize=7)
        ax.tick_params(axis='y', labelsize=7)

        # Legenda sem duplicatas
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), fontsize=8, facecolor='white', edgecolor='black')

        ax.grid(True, linestyle=':', linewidth=0.5, color='lightgray')
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
        <div style="background-color:#f5f5f5;padding:6px 10px;border-radius:10px;text-align:center">
            <h1 style="color:{cor};font-size:36px;margin:4px 0">{valor_atual:.2f}%</h1>
            <p style="color:#444;font-size:13px;margin:2px 0">Percentual IARI</p>
            <p style="color:{cor};font-size:16px;margin:4px 0">{emoji} {texto}</p>
            <p style="color:#333;font-size:11px;margin:2px 0">Meta: {meta:.2f}%</p>
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
