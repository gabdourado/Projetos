#!/bin/bash 

ler_episodios() {
   episodios="episodios.json"
    
    jq -r '.[] | "\(.episodio) | \(.temporada) | \(.titulo) | \(.status)"' "$episodios"

}

while true; do
    read -p ">>> " escolha


    
    case "$escolha" in

        "1")
        ler_episodios
        ;;

        "exit")
        break
        ;;

        "clear")
        clear
        ;;
        
        *)
        echo "Opção Inválida"
        ;;
    esac
done
