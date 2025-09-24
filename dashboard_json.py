import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Frota",
    layout="wide"
)

# --- Função para Carregar e Processar os Dados ---
def carregar_dados():
    try:
        # Alterado para ler o seu arquivo JSON
        df = pd.read_json('registro-database.json')
        
        # Converte a coluna para texto para evitar problemas com números e strings
        # e preenche valores nulos (NaN) caso existam no futuro.
        df['ala_id'] = df['ala_id'].astype(str).fillna('Sem Ala')
        return df
    except FileNotFoundError:
        st.error("Arquivo 'registro-database.json' não encontrado. Por favor, salve o seu JSON neste arquivo.")
        return pd.DataFrame()

# --- Título do Dashboard ---
st.title("🏍️ Dashboard de Frota de Motos")
st.markdown(f"Dados atualizados em: {time.strftime('%d/%m/%Y %H:%M:%S')}")

# --- Carrega os dados ---
df = carregar_dados()

if not df.empty:
    # --- Métricas Principais (KPIs) ---
    st.markdown("### Resumo Geral da Frota")
    
    col1, col2, col3, col4 = st.columns(4)

    # --- Lógica de Cálculo (já funciona para casos "zerados") ---
    # Se o filtro não encontrar nenhuma linha, o resultado de .shape[0] é 0.
    total_motos = len(df)
    motos_disponiveis = df[df['status'] == 'DISPONIVEL'].shape[0]
    motos_manutencao = df[df['status'] == 'MANUTENCAO'].shape[0]
    motos_sem_ala = df[df['ala_id'] == 'Sem Ala'].shape[0]

    # Exibe cada métrica em sua coluna
    col1.metric(label="Motos no Total", value=total_motos)
    col2.metric(label="✅ Disponíveis", value=motos_disponiveis)
    col3.metric(label="🛠️ Em Manutenção", value=motos_manutencao)
    col4.metric(label="❓ Sem Ala", value=motos_sem_ala)

    st.markdown("---")

    # --- Gráficos ---
    st.markdown("### Análise Visual")
    
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.markdown("#### Quantidade de Motos por Ala")
        contagem_por_ala = df['ala_id'].value_counts().reset_index()
        contagem_por_ala.columns = ['ala_id', 'total']
        
        fig_bar, ax_bar = plt.subplots()
        sns.barplot(x='ala_id', y='total', data=contagem_por_ala, ax=ax_bar)
        ax_bar.set_xlabel("Ala")
        ax_bar.set_ylabel("Quantidade de Motos")
        st.pyplot(fig_bar)

    with fig_col2:
        st.markdown("#### Distribuição por Status")
        # value_counts() só vai contar os status que existem.
        # Se só houver "DISPONIVEL", o gráfico mostrará 100% para ele.
        contagem_por_status = df['status'].value_counts()
        
        if not contagem_por_status.empty:
            fig_pie, ax_pie = plt.subplots()
            ax_pie.pie(contagem_por_status, labels=contagem_por_status.index, autopct='%1.1f%%', startangle=90)
            ax_pie.axis('equal')
            st.pyplot(fig_pie)
        else:
            st.write("Não há dados de status para exibir.")
        
    st.markdown("---")
    
    # --- Tabela de Dados Brutos ---
    st.markdown("### Dados Detalhados da Frota")
    st.dataframe(df)