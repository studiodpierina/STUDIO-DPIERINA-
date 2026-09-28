import streamlit as st
import sqlite3
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Studio D'Pierina", page_icon="🎹", layout="centered")

# Conexão com o Banco de Dados
conn = sqlite3.connect('studio_dpierina.db', check_same_thread=False)
c = conn.cursor()

# Criar tabelas se não existirem
c.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        nivel TEXT,
        repertorio TEXT
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS aulas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        dia_semana TEXT,
        horario TEXT,
        mensalidade REAL,
        status TEXT
    )
''')
conn.commit()

# Título Principal
st.title("🎹 Studio D’Pierina")
st.subheader("Gestão de Alunos e Mensalidades")

# Menu de Navegação
aba1, aba2, aba3 = st.tabs(["📋 Cadastrar Aluno", "👥 Lista de Alunos", "💰 Pendências"])

# ABA 1: Cadastrar Aluno
with aba1:
    st.header("Novo Cadastro")
    with st.form("form_aluno", clear_on_submit=True):
        nome = st.text_input("Nome do Aluno")
        telefone = st.text_input("Telefone / WhatsApp")
        nivel = st.selectbox("Nível", ["Iniciante", "Intermediário", "Avançado"])
        repertorio = st.text_input("Peça / Método Atual")
        
        btn_cadastrar = st.form_submit_button("Salvar Aluno")
        
        if btn_cadastrar:
            if nome.strip():
                c.execute("INSERT INTO alunos (nome, telefone, nivel, repertorio) VALUES (?, ?, ?, ?)",
                          (nome, telefone, nivel, repertorio))
                conn.commit()
                st.success(f"Aluno(a) {nome} cadastrado(a) com sucesso!")
            else:
                st.warning("Por favor, preencha o nome do aluno.")

# ABA 2: Lista de Alunos
with aba2:
    st.header("Alunos Cadastrados")
    df_alunos = pd.read_sql_query("SELECT id AS ID, nome AS Nome, telefone AS Telefone, nivel AS Nível, repertorio AS Repertório FROM alunos", conn)
    if not df_alunos.empty:
        st.dataframe(df_alunos, use_container_width=True)
    else:
        st.info("Nenhum aluno cadastrado ainda.")

# ABA 3: Pendências
with aba3:
    st.header("Relatório de Pendências")
    # Exemplo de consulta simples de pendências
    df_pendencias = pd.read_sql_query('''
        SELECT alunos.nome AS Aluno, alunos.telefone AS Telefone, aulas.mensalidade AS Valor
        FROM aulas 
        JOIN alunos ON alunos.id = aulas.aluno_id
        WHERE aulas.status = 'Pendente'
    ''', conn)
    
    if not df_pendencias.empty:
        st.dataframe(df_pendencias, use_container_width=True)
        total = df_pendencias["Valor"].sum()
        st.metric(label="Total Pendente", value=f"R$ {total:.2f}")
    else:
        st.success("Não há pendências registradas!")
