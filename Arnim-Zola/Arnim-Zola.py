#!/home/gab/BCC/Projetos/venv/bin/python

from dotenv import load_dotenv
from os import environ, system
from groq import Groq, GroqError, APIConnectionError, RateLimitError
from time import sleep
from json import load
from subprocess import Popen
from re import split

def carrega_json(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        return load(f)

def print_lento_char(text, delay, cor=None):
    prefixo, sufixo = "", ""
    if cor == "vermelho":
        prefixo, sufixo = "\033[91m", "\033[0m"
    
    for char in text:
        print(f"{prefixo}{char}{sufixo}", end='', flush=True)
        sleep(delay)
    print(" ", end='')

def print_lento_linha(text, delay, cor=None):
    prefixo, sufixo = "", ""
    if cor == "vermelho":
        prefixo, sufixo = "\033[91m", "\033[0m"
    
    for frase in text.split('\n'):
        print(f"{prefixo}{frase}{sufixo}")
        sleep(delay)
        
def falar_e_exibir(texto, delay, cor):
    frases = split(r'(?<=\.)\s*', texto)

    for frase in frases:
        processo = Popen(['espeak', '-v', 'pt-br', '-s', '140', frase])
        print_lento_char(frase, delay, cor)
        processo.wait()

opcoes_geral = """
+-------------------------------------------------------+
|                    SUGESTÕES                          |
+-------------------------------------------------------+
| [c] Conversar com Dr. Arnim Zola via linha de comando |
| [q] Sair                                              |
| [clear] Limpar a tela                                 |
| [help] Mostrar opções novamente                       |
+-------------------------------------------------------+
"""

nome = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⢸⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣦⣤⣀⣀⣤⣤⣀⡀⠀⣀⣠⡆⠀⠀⠀⠀⠀⠀⠤⠒⠛⣛⣛⣻⣿⣶⣾⣿⣦⣄⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠸⠿⢿⣿⣿⣿⣯⣭⣿⣿⣿⣿⣋⣀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣓⠢⠄⢠⡾⢻⣿⣿⣿⣿⡟⠁⠀⠀⠈⠙⢿⣿⣿⣯⡻⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠙⢿⣿⣿⣿⣷⣄⠁⠀⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣷⣌⢧⠀⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⢀⠉⠙⠛⠛⠿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡀⠠⢻⡟⢿⣿⣿⣿⣿⣧⣄⣀⠀⠘⢶⣄⣀⠀⠀⠈⢻⠿⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣾⠀⠀⠀⠻⣈⣙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠲⣄⠀⠀⣀⡤⠤⠀⠀⠀⢠⣿⣿⣿⡿⣿⠇⠀⠀⠐⠺⢉⣡⣴⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣶⣿⣿⣿⣶⣶⡀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣴⣿⣷⣶⣦⣤⡀⠀⢸⣿⣿⣿⠇⠏⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⠟⢿⣿⣿⣿⣷⠀⠹⣿⣿⠿⠿⠛⠻⠿⣿⠇⠀⠀⠀
⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣷⣯⡂⢸⣿⣿⣿⠀⠀⠀⠀⢀⠾⣻⣿⣿⣿⠟⠀⠀⠈⣿⣿⣿⣿⡇⠀⠀⣀⣀⡀⠀⢠⡞⠉⠀⠀⠀⠀
⠀⠀⢸⣟⣽⣿⣯⠀⠀⢹⣿⣿⣿⡟⠼⣿⣿⣿⣇⠀⠀⠀⠠⢰⣿⣿⣿⣿⡄⠀⠀⠀⣸⣿⣿⣿⡇⠀⢀⣤⣼⣿⣷⣾⣷⡀⠀⠀⠀⠀
⠀⢀⣾⣿⡿⠟⠋⠀⠀⢸⣿⣿⣿⣿⡀⢿⣿⣿⣿⣦⠀⠀⠀⢺⣿⣿⣿⣿⣿⣄⠀⠀⣿⣿⣿⣿⡇⠐⣿⣿⣿⣿⠿⣿⣿⡿⣦⠀⠀⠀
⠀⢻⣿⠏⠀⠀⠀⠀⢠⣿⣿⣿⡟⡿⠀⠀⢻⣿⣿⣿⣷⣤⡀⠘⣷⠻⣿⣿⣿⣿⣷⣼⣿⣿⣿⣿⣇⣾⣿⣿⣿⠁⠀⢼⣿⣿⣿⣆⠀⠀
⠀⠀⠈⠀⠀⠀⠀⠀⢸⣿⣿⣿⡗⠁⠀⠀⠀⠙⢿⣿⣿⣿⣿⣷⣾⣆⡙⣿⣿⣿⣿⣿⣿⣿⣿⣿⠌⣾⣿⣿⣿⣆⠀⠀⠀⠉⠻⣿⡷⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠘⣟⣿⣿⣿⡆⠀⠀⠀⠀⠙⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣶⣤⣤⣤⣀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⢈⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣠⣤⣤⣶⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣠⣤⣄⠀⠠⢶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣀⠀⣠⣀⡠⠞⣿⣿⣿⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣿⣷⣦⣄⣀⢿⡽⢻⣦
⠻⠶⠾⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠋
 “Se cortar uma cabeça, duas nascerão no lugar.” 
"""

def intro():
    system('clear')
    print_lento_char("...", 0.5, "vermelho")
    sleep(0.75)
    print_lento_char(nome, 0.0025, "vermelho")
    falar_e_exibir("\nSou o Dr. Arnim Zola, um cientista da Hydra. Não sou uma gravação. Eu existo!", 0.1, "vermelho")
    sleep(0.25)
    print_lento_linha(opcoes_geral, 0.025, "vermelho")

def menu():
     while True:
        escolha = input("\033[92m>>> \033[0m")

        match escolha:
            case "c":
                system('clear')
                personalidade = carrega_json('./system_message.json')
                assistente(personalidade)
                falar_e_exibir("Adeus!", 0.1, "vermelho")
                print_lento_char("\nPara ver novamente as opções use [help].", 0.025, "vermelho")
                print()
                
            case "q":
                print_lento_char("Saindo...", 0.025,"vermelho")
                print()
                break
            
            case "clear":
                system('clear')

            case "help":
                print_lento_linha(opcoes_geral, 0.025, "vermelho")
                
            case _:
                print("Opção inválida. Tente novamente.\n")

def assistente(personalidade):
    load_dotenv()

    api_key = environ.get("GROQ_API_KEY")
    if not api_key:
        print_lento_char("Chave de API não encontrada.", 0.025)
        return

    try:
        client = Groq(api_key=api_key)

    except Exception:
        print_lento_char("Erro ao inicializar cliente Groq\n", 0.025)
        return

    falar_e_exibir("[exit] Para sair do modo interativo.", 0.1, "vermelho")
    falar_e_exibir("\nO que você quer saber?", 0.1, "vermelho")

    messages = personalidade

    while True:
        pergunta = input("\033[92m\n>>> \033[0m")

        if pergunta.lower() == 'exit':
            break

        if not pergunta.strip():
            continue

        messages.append({"role": "user", "content": pergunta})

        try:
            resposta = client.chat.completions.create(
                messages = messages,
                model="llama3-70b-8192"
            ).choices[0].message.content

            messages.append({"role": "assistant", "content": resposta})
            falar_e_exibir(">>> " + resposta, 0.1, "vermelho")

        except RateLimitError:
            print_lento_char("Limite de requisições atingido. Tente novamente em breve.\n", 0.025)
            break

        except APIConnectionError:
            print_lento_char("Erro de conexão com a API da Groq. Verifique sua internet.\n", 0.025)
            break

        except GroqError:
            print_lento_char(f"Erro da API Groq\n", 0.025)
            break

        except Exception :
            print_lento_char(f"Erro inesperado\n", 0.025)
            break

if __name__ == "__main__":
    intro()
    menu()