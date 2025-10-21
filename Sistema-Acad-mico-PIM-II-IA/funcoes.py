import sqlite3

# === CONEXÃO E CONFIGURAÇÃO INICIAL ===
def conectar():
    return sqlite3.connect("sistema_academico.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de usuários (professores e alunos)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT,
        matricula TEXT,
        senha TEXT NOT NULL,
        tipo_usuario TEXT NOT NULL,
        materia TEXT
    )
    """)

    # Tabelas de notas por matéria
    materias = ["matematica", "portugues", "ciencias", "geografia"]
    for materia in materias:
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {materia} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT,
            np1 REAL,
            np2 REAL,
            pim REAL
        )
        """)

    # Tabela de presença
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS presencas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT,
        data TEXT,
        presente INTEGER
    )
    """)

    # Cronograma
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cronograma (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sala TEXT,
        data TEXT,
        dia_semana TEXT,
        conteudo TEXT
    )
    """)

    conn.commit()
    conn.close()


# === CADASTRO E LOGIN ===
def adicionar_usuario(nome, email, matricula, senha, tipo_usuario, materia=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO usuarios (nome, email, matricula, senha, tipo_usuario, materia)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, email, matricula, senha, tipo_usuario, materia))
    conn.commit()
    conn.close()

def verificar_login(email_ou_matricula, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM usuarios WHERE (email = ? OR matricula = ?) AND senha = ?
    """, (email_ou_matricula, email_ou_matricula, senha))
    user = cursor.fetchone()
    conn.close()
    return user


# === FUNÇÕES PROFESSOR ===
def cadastrar_nota(materia, matricula, np1=None, np2=None, pim=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {materia} WHERE matricula = ?", (matricula,))
    existe = cursor.fetchone()

    if existe:
        cursor.execute(f"""
            UPDATE {materia}
            SET np1 = COALESCE(?, np1),
                np2 = COALESCE(?, np2),
                pim = COALESCE(?, pim)
            WHERE matricula = ?
        """, (np1, np2, pim, matricula))
    else:
        cursor.execute(f"""
            INSERT INTO {materia} (matricula, np1, np2, pim)
            VALUES (?, ?, ?, ?)
        """, (matricula, np1, np2, pim))
    conn.commit()
    conn.close()

def consultar_notas(materia, matricula):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT np1, np2, pim FROM {materia} WHERE matricula = ?", (matricula,))
    notas = cursor.fetchone()
    conn.close()
    return notas

def atualizar_presenca(matricula, data, presente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO presencas (matricula, data, presente) VALUES (?, ?, ?)", (matricula, data, presente))
    conn.commit()
    conn.close()

def consultar_presenca(matricula):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT data, presente FROM presencas WHERE matricula = ?", (matricula,))
    dados = cursor.fetchall()
    conn.close()
    return dados

def adicionar_aula_cronograma(sala, data, dia_semana, conteudo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO cronograma (sala, data, dia_semana, conteudo)
    VALUES (?, ?, ?, ?)
    """, (sala, data, dia_semana, conteudo))
    conn.commit()
    conn.close()

def consultar_cronograma():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT sala, data, dia_semana, conteudo FROM cronograma")
    cronogramas = cursor.fetchall()
    conn.close()
    return cronogramas