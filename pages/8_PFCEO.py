import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- CONFIGURAÇÃO GERAL ---
st.set_page_config(
    page_title="Dashboard PFCEO - RECAP",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- TÍTULO DO DASHBOARD ---
st.markdown("## Dashboard de PFCEO - RECAP")

# --- CAMINHO DO ARQUIVO ---
ARQUIVO = "historico_recap.xlsx"

# --- LEITURA E TRATAMENTO DOS DADOS ---
if os.path.exists(ARQUIVO):
    df = pd.read_excel(ARQUIVO, sheet_name="PFCEO")
    df.columns = df.columns.str.strip().str.upper()
    df["SEMANA"] = df["SEMANA"].astype(str)
    df = df.sort_values("SEMANA")

    ultimo = df.iloc[-1]
    semana = ultimo["SEMANA"]
    valor_atual = float(ultimo["EQUIPAMENTOS NO PAINEL"])
    meta = float(ultimo["META"])

    if "% AMEAÇAS INDICADOR MÊS" in df.columns:
        df["AMEACA_MES"] = df["% AMEAÇAS INDICADOR MÊS"].astype(float)
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
        st.markdown("#### Histórico de PFCEO")

        fig, ax = plt.subplots(figsize=(8, 4), facecolor='white')

        semanas = df["SEMANA"].tolist()
        valores = df["EQUIPAMENTOS NO PAINEL"].astype(float).tolist()
        ameacas = df["AMEACA_MES"].tolist()

        abaixo_meta = [v if v <= meta else meta for v in valores]
        acima_meta = [v if v > meta else np.nan for v in valores]

        ax.fill_between(semanas, abaixo_meta, color="#1f77b4", alpha=0.5, label="Abaixo da Meta")
        ax.fill_between(semanas, acima_meta, color="red", alpha=0.3, label="Acima da Meta")
        ax.plot(semanas, valores, color="#1f77b4", marker='o', linewidth=1)

        for i, proj in enumerate(ameacas):
            if not np.isnan(proj):
                ax.plot(semanas[i], proj, marker='o', color="orange", markersize=6, label="Ameaça Mês" if i == 0 else "")

        ax.axhline(y=meta, color='gray', linestyle='--', linewidth=1, label=f"Meta = {meta:.2f}")

        ax.set_facecolor('white')
        ax.set_ylabel("Equipamentos no Painel", color='black', fontsize=10)
        ax.set_xlabel("Semana", color='black', fontsize=10)
        ax.tick_params(axis='x', colors='black', rotation=45, labelsize=8)
        ax.tick_params(axis='y', colors='black', labelsize=8)

        # Melhorar visualização do eixo Y (valor mínimo dinâmico com base nos dados)
        y_min = max(0, min(valores + [meta]) - 2)
        ax.set_ylim(bottom=y_min, top=max(valores + [meta]) + 2)

        ax.set_xticks(range(0, len(semanas), 3))
        ax.set_xticklabels([semanas[i] for i in range(0, len(semanas), 3)])

        ax.legend(facecolor='white', edgecolor='black', labelcolor='black', fontsize=8)
        ax.grid(True, linestyle=':', linewidth=0.5, color='lightgray')

        fig.tight_layout()
        st.pyplot(fig)

    # --- KPI + RESUMO ---
    with col2:
        st.markdown(f"#### Semana {semana}")

        if valor_atual <= meta:
            cor = "#1f77b4"
            emoji = "✅"
            texto = "Dentro da meta"
        else:
            cor = "red"
            emoji = "⚠️"
            texto = "Acima da meta"

        st.markdown(f"""
        <div style="background-color:#f5f5f5;padding:6px 10px;border-radius:10px;text-align:center">
            <h1 style="color:{cor};font-size:36px;margin:4px 0">{valor_atual:.2f}</h1>
            <p style="color:#444;font-size:13px;margin:2px 0">Equipamentos no Painel</p>
            <p style="color:{cor};font-size:16px;margin:4px 0">{emoji} {texto}</p>
            <p style="color:#333;font-size:11px;margin:2px 0">Meta: {meta:.2f}</p>
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
