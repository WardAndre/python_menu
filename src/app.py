import json
import os
import datetime

linha_esmeralda = [
    {
        "nome": "Osasco",
        "conexão": "Linha Diamante",
        "alertas": [
            {
                "email": "jose@mail.com",
                "assunto": "Catraca",
                "mensagem": "Umas das catracas estava quebrada, aumentando tempo de acesso a estação"
            }
        ]
    },
    {
        "nome": "Presidente Altino",
        "conexão": "Linha Diamante",
        "alertas": []
    },
    {
        "nome": "Ceasa",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Villa-Lobos Jaguaré",
        "conexão": None,
        "alertas": [
            {
                "email": "test@gmail.com",
                "assunto": "Manutenção",
                "mensagem": "Um dos bancos estava quebrado e jogado ao lado de uma das escadas"
            }
        ]
    },
    {
        "nome": "Cidade Universitária",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Pinheiros",
        "conexão": "Linha Amarela",
        "alertas": []
    },
    {
        "nome": "Hebraica Rebouças",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Cidade Jardim",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Vila Olímpia",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Berrini",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Morumbi",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Granja Julieta",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "João Dias",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Santo Amaro",
        "conexão": "Linha Lilás",
        "alertas": []
    },
    {
        "nome": "Socorro",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Jurubatuba",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Autódromo",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Primavera Interlagos",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Grajaú",
        "conexão": None,
        "alertas": []
    },
    {
        "nome": "Mendes Vila Natal",
        "conexão": None,
        "alertas": []
    }
]

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
    print("4 - Salvar informações")
    print("5 - Sair\n")

def salvar_informacoes(arr):
    exibir_titulo("Salvar informações sobre a linha esmeralda")
    print("Salvando informações...")
    try:
        with open("Linha_esmeralda_infos.json", "w", encoding="utf-8") as arq:
            json.dump(linha_esmeralda, arq, ensure_ascii=False, indent=4)
        print("Arquivo salvo com sucesso!")
    except:
        print("Não foi possível salvar as informações")
    voltar_menu_principal()

def salvar_trajeto(dic):
    try:
        if not os.path.exists("trajeto_historico.json"):  # Se o arquivo não existir
            with open("trajeto_historico.json", "w", encoding="utf-8") as arq:
                json.dump(dic, arq, ensure_ascii=False, indent=4)
            print("Trajeto salvo com sucesso!")
            return
        with open("trajeto_historico.json", "r", encoding="utf-8") as arq:
            try:
                content = json.load(arq)
                if isinstance(content, dict):
                    content = [content]
                elif not isinstance(content, list):
                    content = []
            except json.JSONDecodeError:
                content = []
        content.append(dic)
        with open("trajeto_historico.json", "w", encoding="utf-8") as arq:
            json.dump(content, arq, ensure_ascii=False, indent=4)
        print("Trajeto salvo com sucesso!")
    except:
        print("Não foi possível salvar o trajeto")

def calcular_tempo_viagem():
    exibir_titulo("Calcular tempo de viagem")
    partida_encontrada = False
    destino_encontrado = False
    partida_nome = ""
    destino_nome = ""
    partida_index = None
    destino_index = None
    estacao_partida = input("Informar estação de partida: ").lower()
    for i in linha_esmeralda:
        if i["nome"].lower() == estacao_partida:
            partida_encontrada = True
            partida_nome = i["nome"]
            partida_index = linha_esmeralda.index(i)
            estacao_destino = input("Informar estação de destino: ").lower()
            for j in linha_esmeralda:
                if j["nome"].lower() == estacao_destino:
                    destino_encontrado = True
                    destino_nome = j["nome"]
                    destino_index = linha_esmeralda.index(j)
            if not destino_encontrado:
                print("Estação não encontrada!")
    if not partida_encontrada:
        print("Estação não encontrada!")
    if partida_encontrada and destino_encontrado:
        segundos_parado_estacao = 30
        segundos_trajeto_entre_estacoes = 120
        if partida_index > destino_index:
            trajeto_reverso = list(reversed(linha_esmeralda[destino_index : partida_index + 1]))
            tempo_total = ((segundos_parado_estacao * len(trajeto_reverso)) + (
                    segundos_trajeto_entre_estacoes * len(list(trajeto_reverso)) - 1)) / 60
            print(f"\nTempo total do trajeto entre {partida_nome} e {destino_nome}: {tempo_total:.2f} minutos")
        else:
            trajeto = linha_esmeralda[partida_index : destino_index + 1]
            tempo_total = ((segundos_parado_estacao * len(trajeto)) + (
                    segundos_trajeto_entre_estacoes * len(trajeto) - 1)) / 60
            print(f"\nTempo total do trajeto entre {partida_nome} e {destino_nome}: {tempo_total:.2f} minutos")
        trajeto_dic = {
            "data": datetime.datetime.today().strftime('%m/%d/%Y'),
            "partida": partida_nome,
            "destino": destino_nome,
            "tempo total": f"{tempo_total:.2f} minutos"
        }
        salvar_trajeto(trajeto_dic)
    voltar_menu_principal()

def listar_alertas():
    exibir_titulo("Alertas e avisos")
    for i in linha_esmeralda:
        if len(i["alertas"]):
            print(f"\n#### {i["nome"]} ####\n")
        for j in i["alertas"]:
            for key, value in j.items():
                print(f"{key}: {value}")
            print("-------------------")
    voltar_menu_principal()

def enviar_alerta():
    exibir_titulo("Enviar alerta")
    estacao = input("Digite a estação que deseja enviar um alerta: ").lower()
    estacao_encontrada = False
    for i in linha_esmeralda:
        if i["nome"].lower() == estacao:
            estacao_encontrada = True
            email = input("Digite seu e-mail: ")
            assunto = input("O assunto do alerta: ")
            mensagem = input("Digite sua mensagem de alerta: ")
            alerta ={
                "email": email,
                "assunto": assunto,
                "mensagem": mensagem
            }
            i["alertas"].append(alerta)
    if not estacao_encontrada:
        print("Estação não encontrada!")
    voltar_menu_principal()

def finalizar_app():
    exibir_titulo("Finalizando o programa")

def escolher_opcao():
    try:
        option = int(input("Escolha uma opção (1 a 5): "))
        match option:
            case 1:
                calcular_tempo_viagem()
            case 2:
                listar_alertas()
            case 3:
                enviar_alerta()
            case 4:
                salvar_informacoes(linha_esmeralda)
            case 5:
                finalizar_app()
            case _:
                opcao_invalida()
    except:
        opcao_invalida()

def voltar_menu_principal():
    input("\nDigite uma tecla para voltar ao menu principal: ")
    main()

def opcao_invalida():
    print("Opção inválida")
    voltar_menu_principal()

def exibir_titulo(string):
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
    print("*" * len(string))
    print(string)
    print("*" * len(string))
    print()

def main():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
    exibir_nome_programa()
    exibir_opcoes()
    escolher_opcao()

if __name__ == "__main__":
    main()
