from funcoes import (
    criar_tabelas, adicionar_usuario, verificar_login,
    cadastrar_nota, consultar_notas, atualizar_presenca,
    consultar_presenca, adicionar_aula_cronograma,
    consultar_cronograma
)

# === SISTEMA PRINCIPAL ===
class SistemaAcademico:
    def __init__(self):
        criar_tabelas()

    # --- ÁREA DO PROFESSOR ---
    def area_professor(self, professor):
        materia = professor[6]  # matéria do professor no banco
        print(f"\n🎓 Bem-vindo, Professor {professor[1]} — Matéria: {materia.capitalize()}")

        while True:
            print("""
--- Área do Professor ---
1. Lançar notas
2. Atualizar presença
3. Gerar relatório
4. Gerenciar cronograma
5. Bloco do professor
6. Sair
""")
            opc = input("Escolha uma opção: ").strip()

            if opc == "1":
                self.lancar_notas(materia)
            elif opc == "2":
                self.atualizar_presenca()
            elif opc == "3":
                self.gerar_relatorio(materia)
            elif opc == "4":
                self.gerenciar_cronograma()
            elif opc == "5":
                self.bloco_professor()
            elif opc == "6":
                break
            else:
                print("❌ Opção inválida.")

    def lancar_notas(self, materia):
        print(f"\n📘 Lançamento de Notas — {materia.capitalize()}")
        matricula = input("Digite a matrícula do aluno: ").strip()
        np1 = float(input("Nota NP1: "))
        np2 = float(input("Nota NP2: "))
        pim = float(input("Nota PIM: "))
        cadastrar_nota(materia, matricula, np1, np2, pim)
        print("✅ Notas lançadas com sucesso!")

    def atualizar_presenca(self):
        matricula = input("Matrícula do aluno: ").strip()
        data = input("Data (ex: 14/10/2025): ").strip()
        presente = int(input("Presente? (1=Sim, 0=Não): "))
        atualizar_presenca(matricula, data, presente)
        print("✅ Presença atualizada com sucesso!")

    def gerar_relatorio(self, materia):
        matricula = input("Matrícula do aluno: ").strip()
        notas = consultar_notas(materia, matricula)
        presencas = consultar_presenca(matricula)
        print(f"\n📄 Relatório — {matricula}")
        if notas:
            print(f"Notas: NP1={notas[0]} | NP2={notas[1]} | PIM={notas[2]}")
        else:
            print("Nenhuma nota registrada.")
        print("Presenças:")
        for data, pres in presencas:
            print(f"{data} - {'Presente' if pres else 'Faltou'}")

    def gerenciar_cronograma(self):
        while True:
            print("""
--- Gerenciar Cronograma ---
1. Ver cronograma
2. Adicionar aula
3. Voltar
""")
            opc = input("Escolha: ").strip()
            if opc == "1":
                cronos = consultar_cronograma()
                for sala, data, dia, conteudo in cronos:
                    print(f"Sala {sala} | {data} ({dia}) | {conteudo}")
            elif opc == "2":
                sala = input("Sala: ").strip()
                data = input("Data: ").strip()
                dia = input("Dia da semana: ").strip()
                conteudo = input("Conteúdo: ").strip()
                adicionar_aula_cronograma(sala, data, dia, conteudo)
                print("✅ Aula adicionada com sucesso!")
            elif opc == "3":
                break
            else:
                print("❌ Inválido!")

    def bloco_professor(self):
        print("\n🗒️ Bloco do Professor — anote livremente.")
        print("(Digite 'sair' para encerrar)")
        with open("bloco_professor.txt", "a", encoding="utf-8") as f:
            while True:
                texto = input("> ")
                if texto.lower() == "sair":
                    break
                f.write(texto + "\n")
        print("✅ Anotações salvas!")

    # --- ÁREA DO ALUNO ---
    def area_aluno(self, aluno):
        print(f"\n🎓 Bem-vindo, {aluno[1]}!")
        while True:
            print("""
--- Área do Aluno ---
1. Ver notas
2. Ver presenças
3. Ver cronograma
4. Bloco do aluno
5. Sair
""")
            opc = input("Escolha: ").strip()

            if opc == "1":
                self.ver_notas(aluno)
            elif opc == "2":
                self.ver_presencas(aluno)
            elif opc == "3":
                self.ver_cronograma()
            elif opc == "4":
                self.bloco_aluno(aluno)
            elif opc == "5":
                break
            else:
                print("❌ Opção inválida.")

    def ver_notas(self, aluno):
        materias = ["matematica", "portugues", "ciencias", "geografia"]
        print("\nMatérias disponíveis:")
        for i, m in enumerate(materias, start=1):
            print(f"{i}. {m.capitalize()}")
        escolha = int(input("Selecione uma matéria: "))
        materia = materias[escolha - 1]
        notas = consultar_notas(materia, aluno[3])
        if notas:
            print(f"\n📘 {materia.capitalize()} - NP1: {notas[0]} | NP2: {notas[1]} | PIM: {notas[2]}")
        else:
            print("Nenhuma nota registrada.")

    def ver_presencas(self, aluno):
        presencas = consultar_presenca(aluno[3])
        print("\n📅 Presenças:")
        for data, pres in presencas:
            print(f"{data} - {'Presente' if pres else 'Faltou'}")

    def ver_cronograma(self):
        print("\n📖 Cronograma de Aulas:")
        cronos = consultar_cronograma()
        for sala, data, dia, conteudo in cronos:
            print(f"Sala {sala} | {data} ({dia}) | {conteudo}")

    def bloco_aluno(self, aluno):
        print("\n📔 Bloco do Aluno — suas anotações pessoais.")
        arquivo = f"bloco_{aluno[3]}.txt"
        print("(Digite 'sair' para encerrar)")
        with open(arquivo, "a", encoding="utf-8") as f:
            while True:
                texto = input("> ")
                if texto.lower() == "sair":
                    break
                f.write(texto + "\n")
        print("✅ Anotações salvas!")

# === EXECUÇÃO PRINCIPAL ===
sistema = SistemaAcademico()

while True:
    print("""
===== SISTEMA ACADÊMICO =====
1. Cadastrar usuário
2. Login
3. Sair
""")
    escolha = input("Escolha: ").strip()

    if escolha == "1":
        nome = input("Nome: ")
        email = input("Email (ou deixe em branco se for aluno): ")
        matricula = input("Matrícula (ou deixe em branco se for professor): ")
        senha = input("Senha: ")
        if "@prof" in email:
            tipo_usuario = "professor"
            if "@profmatematica" in email:
                materia = "matematica"
            elif "@profportugues" in email:
                materia = "portugues"
            elif "@profciencias" in email:
                materia = "ciencias"
            elif "@profgeografia" in email:
                materia = "geografia"
            else:
                materia = None
        else:
            tipo_usuario = "aluno"
            materia = None
        adicionar_usuario(nome, email, matricula, senha, tipo_usuario, materia)
        print("✅ Usuário cadastrado com sucesso!")

    elif escolha == "2":
        login = input("Email ou Matrícula: ")
        senha = input("Senha: ")
        usuario = verificar_login(login, senha)

        if usuario:
            if usuario[5] == "professor":
                sistema.area_professor(usuario)
            else:
                sistema.area_aluno(usuario)
        else:
            print("❌ Login inválido!")

    elif escolha == "3":
        print("Saindo do sistema...")
        break
    else:
        print("❌ Opção inválida!")