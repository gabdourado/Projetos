#!/home/gab/BCC/Projetos/venv/bin/python

from prettytable import PrettyTable
from time import sleep
from json import load, dump
from random import choice
from os import system

def slow_print_character(text, delay):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)

def slow_print_frase(text, delay):
    for farse in text.split('\n'):
        print(farse, end='\n', flush=True)
        sleep(delay)

opcoes = """
+--------------------------------------------+
|                  OPÇÕES                    |
+--------------------------------------------+
| [1] Listar todos os episódios              |
| [2] Sortear um episódio aleatório          |
| [3] Marcar um episódio como assistido      |
| [4] Marcar um episódio como não assistido  |
| [5] Resetar lista                          |
| [q] Sair                                   |
| [clear] Limpar a tela                      |
| [help] Mostrar opções novamente            |                     
+--------------------------------------------+
"""

def intro():
    ascii_art = r"""
______   _                  _       ___  ___  _                              
| ___ \ | |                | |      |  \/  | (_)                             
| |_/ / | |   __ _    ___  | | __   | .  . |  _   _ __   _ __    ___    _ __ 
| ___ \ | |  / _` |  / __| | |/ /   | |\/| | | | | '__| | '__|  / _ \  | '__|
| |_/ / | | | (_| | | (__  |   <    | |  | | | | | |    | |    | (_) | | |   
\____/  |_|  \__,_|  \___| |_|\_\   \_|  |_/ |_| |_|    |_|     \___/  |_| 
"""

    slow_print_character("...", 0.5)
    sleep(0.75)
    slow_print_character(ascii_art, 0.0025)
    slow_print_character("\nBem-vindo ao gerenciador de episódios de Black Mirror:\n", 0.025)
    sleep(0.25)
    slow_print_frase(opcoes, 0.025)

def carregar_episodios():
    with open("episodios.json", "r", encoding="utf-8") as f:
        return load(f)

def salvar_episodios(episodios):
    with open("episodios.json", "w", encoding="utf-8") as f:
        dump(episodios, f, ensure_ascii=False, indent=2)


def listar_episodios(episodios):
    table = PrettyTable()
    table.field_names = ["Titulo", "Temporada", "Episódio", "Status"]

    for i in range(len(episodios)):
        table.add_row([episodios[i]['titulo'], episodios[i]['temporada'], episodios[i]['episodio'], episodios[i]['status']])
    
    slow_print_frase(str(table), 0.025)

def episodio_aleatorio(episodios):
    nao_assistidos = [ep for ep in episodios if ep["status"] == "❌ Não assistido"]

    sorteado = choice(nao_assistidos)

    table = PrettyTable()
    table.field_names = ["Titulo", "Temporada", "Episódio"]
    table.add_row([sorteado['titulo'], sorteado['temporada'], sorteado['episodio']])
    
    slow_print_frase(str(table), 0.025)


def encontrar_episodio(temp, ep, episodios):
    if temp < 1 or ep < 1:
        print("Temporada ou episódio inválido!")
        return None

    eps_temp = [e for e in episodios if e["temporada"] == temp]
    if not eps_temp:
        print("Temporada inexistente.")
        return None

    for e in eps_temp:
        if e["episodio"] == ep:
            return e

    print("Episódio inexistente.")
    return None


def altera_status(episodios, temp, ep, flag):
    episodio = encontrar_episodio(temp, ep, episodios)

    if not episodio:
        return

    match flag:
        case 3:
            episodio["status"] = "✅ Assistido"
            print(f"T{temp}E{ep} marcado como assistido!")
        case 4:
            episodio["status"] = "❌ Não assistido"
            print(f"T{temp}E{ep} marcado como não assistido!")

    salvar_episodios(episodios)
    
def reseta_lista(episodios):
    for ep in episodios: ep['status'] = '❌ Não assistido'

    salvar_episodios(episodios)

def temp_e_ep():
    try:
        print("Temporada:")
        temp = int(input(">>> "))
        print("Episódio:")
        ep = int(input(">>> "))
        return temp, ep
    
    except ValueError:
        print("Entrata inválida")
        return None, None

def escolha(episodios):
    while True:
        escolha = input(">>> ")

        match escolha:
            case "1":
                listar_episodios(episodios)

            case "2":
                episodio_aleatorio(episodios)

            case "3":
                temp, ep = temp_e_ep()
                if temp and ep:
                    altera_status(episodios, temp, ep, 3)

            case "4":
                temp, ep = temp_e_ep()
                if temp and ep:
                    altera_status(episodios, temp, ep, 4)

            case "5":
                print("Tem certeza que deseja alterar tudo? [y/n] ")
                escolha = input(">>> ")
                if escolha.lower() == 'y':
                    reseta_lista(episodios)
                else:
                    continue
            case "q":
                print("Saindo...")
                break
            
            case "clear":
                system('clear')

            case "help":
                slow_print_frase(opcoes, 0.025)
                
            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    episodios = carregar_episodios()
    intro()
    escolha(episodios)