import json
import os
import datetime

import banco

def exibir_nome_programa():
    print("""
    █▀▀ █▀▀ █▀█   ▄▄   █░░ █ █▄░█ █░█ ▄▀█   █▀▀ █▀ █▀▄▀█ █▀▀ █▀█ ▄▀█ █░░ █▀▄ ▄▀█
    █▄▄ █▄▄ █▀▄   ░░   █▄▄ █ █░▀█ █▀█ █▀█   ██▄ ▄█ █░▀░█ ██▄ █▀▄ █▀█ █▄▄ █▄▀ █▀█
    Osasco / Presidente Altino / Ceasa / Villa-Lobos Jaguaré / Cidade Universitária
    Pinheiros / Hebraica Rebouças / Cidade Jardim / Vila Olimpia / Berrini
    Morumbi / Granja Julieta / João Dias / Santo Amaro / Socorro / Jurubatuba
    Autódromo / Primavera Interlagos / Grajaú / Mendes Vila Natal
""")

def exibir_opcoes():
    print("1 - Calcular tempo de viagem")
    print("2 - Listar alertas")
    print("3 - Enviar alerta")
    print("4 - Salvar informações em JSON")
    print("5 – Alterar / Deletar alerta")
    print("6 - Sair\n")

def salvar_informacoes():
    exibir_titulo("Salvar informações sobre a linha esmeralda")
    print("Salvando informações...")
    try:
        dados = banco.consultar_linha_esmeralda()
        with open("Linha_esmeralda_infos.json", "w", encoding="utf-8") as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)
        print("Arquivo salvo com sucesso!")
    except:
        print("Não foi possível salvar as informações")

def salvar_trajeto(dicionario):
    try:
        if not os.path.exists("trajeto_historico.json"):
            with open("trajeto_historico.json", "w", encoding="utf-8") as arq:
                json.dump(dicionario, arq, ensure_ascii=False, indent=4)
            print("Trajeto salvo com sucesso!")
            return
        with open("trajeto_historico.json", "r", encoding="utf-8") as arq:
            try:
                conteudo = json.load(arq)
                if isinstance(conteudo, dict):
                    conteudo = [conteudo]
                elif not isinstance(conteudo, list):
                    conteudo = []
            except json.JSONDecodeError:
                conteudo = []
        conteudo.append(dicionario)
        with open("trajeto_historico.json", "w", encoding="utf-8") as arq:
            json.dump(conteudo, arq, ensure_ascii=False, indent=4)
        print("Trajeto salvo com sucesso!")
    except:
        print("Não foi possível salvar o trajeto")

def calcular_tempo_viagem():
    exibir_titulo("Calcular tempo de viagem")
    estacoes_raw = banco.consultar_estacoes()
    nomes = [t[1] for t in estacoes_raw]
    nomes_lower = [n.lower() for n in nomes]
    partida_input = input("Informar estação de partida: ").strip().lower()
    if partida_input not in nomes_lower:
        print("Estação não encontrada!")
        return
    destino_input = input("Informar estação de destino: ").strip().lower()
    if destino_input not in nomes_lower:
        print("Estação não encontrada!")
        return
    partida_index = nomes_lower.index(partida_input)
    destino_index = nomes_lower.index(destino_input)
    segundos_parado = 30
    segundos_entre = 120
    if partida_index > destino_index:
        trecho = nomes[destino_index:partida_index + 1][::-1]
    else:
        trecho = nomes[partida_index:destino_index + 1]
    tempo_total_min = (
        segundos_parado * len(trecho)
        + segundos_entre * (len(trecho) - 1)
    ) / 60
    partida_nome = nomes[partida_index]
    destino_nome = nomes[destino_index]
    print(f"\nTempo total do trajeto entre {partida_nome} e {destino_nome}: {tempo_total_min:.2f} minutos")
    trajeto_dic = {
        "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "partida": partida_nome,
        "destino": destino_nome,
        "tempo_total_minutos": round(tempo_total_min, 2)
    }
    salvar_trajeto(trajeto_dic)

def listar_alertas():
    exibir_titulo("Alertas e avisos")
    estacoes = banco.consultar_linha_esmeralda()
    for estacao in estacoes:
        nome = estacao.get("nome")
        alertas = estacao.get("alertas", [])
        print(f"\n#### {nome} ####\n")
        if not alertas:
            print("Nenhum alerta para esta estação.")
        else:
            for idx, alerta in enumerate(alertas, start=1):
                print(f"Alerta {idx}:")
                print(f"  E-mail   : {alerta.get('email')}")
                print(f"  Assunto  : {alerta.get('assunto')}")
                print(f"  Mensagem : {alerta.get('mensagem')}")
                print("-------------------")

def enviar_alerta():
    nome_est = input("Digite o nome da estação: ").strip()
    est = banco.obter_estacao_por_nome(nome_est)
    if not est:
        print(f"Estação '{nome_est}' não encontrada.")
        return
    id_est = est[0]
    email   = input("E-mail: ").strip()
    assunto = input("Assunto do alerta: ").strip()
    mensagem= input("Mensagem do alerta: ").strip()
    alerta = {
        "email":    email,
        "assunto":  assunto,
        "mensagem": mensagem,
        "id_estacao": id_est
    }
    banco.inserir_alerta(alerta)
    print("Alerta salvo com sucesso!")

def exibir_titulo(string):
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
    print("*" * len(string))
    print(string)
    print("*" * len(string))
    print()

def alterar_deletar_alerta():
    exibir_titulo("Alterar / Deletar alertas")
    alertas = banco.consultar_todos_alertas()
    if not alertas:
        print("Nenhum alerta cadastrado.")
        return
    print(f"{'ID':<4} {'Estação':<20} {'Assunto'}")
    print("-" * 50)
    for id_a, nome_est, _, assunto, _ in alertas:
        print(f"{id_a:<4} {nome_est:<20} {assunto}")
    escolha_id = input("\nDigite o ID do alerta (0 p/ cancelar): ").strip()
    if not escolha_id.isdigit():
        print("Entrada inválida.")
        return
    id_sel = int(escolha_id)
    if id_sel == 0:
        return
    original = next((a for a in alertas if a[0] == id_sel), None)
    if original is None:
        print("ID não encontrado.")
        return
    _, nome_est, email_atual, assunto_atual, mensagem_atual = original
    modo = input("Digite (A)lterar ou (D)eletar: ").strip().upper()
    if modo == "A":
        novo_email   = input(f"E-mail   [{email_atual}]: ").strip() or email_atual
        novo_assunto = input(f"Assunto  [{assunto_atual}]: ").strip() or assunto_atual
        nova_msg     = input(f"Mensagem [{mensagem_atual}]: ").strip() or mensagem_atual
        banco.atualizar_alerta(id_sel, novo_email, novo_assunto, nova_msg)
        print("Alerta atualizado com sucesso!")
    elif modo == "D":
        confirma = input("Confirma exclusão deste alerta? (S/N): ").strip().upper()
        if confirma == "S":
            banco.deletar_alerta(id_sel)
            print("Alerta deletado com sucesso!")
        else:
            print("Operação cancelada.")
    else:
        print("Opção inválida.")

def main():
    while True:
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
        exibir_nome_programa()
        exibir_opcoes()
        escolha = input("Escolha uma opção (1 a 6): ").strip()
        if escolha == "1":
            calcular_tempo_viagem()
        elif escolha == "2":
            listar_alertas()
        elif escolha == "3":
            enviar_alerta()
        elif escolha == "4":
            salvar_informacoes()
        elif escolha == "5":
            alterar_deletar_alerta()
        elif escolha == "6":
            print("Finalizando o programa…")
            break
        else:
            print("Opção inválida.")

        input("\nDigite uma tecla para voltar ao menu principal: ")

if __name__ == "__main__":
    main()
