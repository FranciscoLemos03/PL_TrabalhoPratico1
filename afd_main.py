import json
import sys
import graphviz
import graphviz #doctest: +NO_EXE

# Abrir ficheiro AFD.json
def load_dfa(file_path):
    with open(file_path, 'r') as f:
        dfa = json.load(f)
    return dfa

# Validar se a palavra segue o caminho do AFD.JSON
def is_valid_word(dfa, word, state='q0', path=[]):
    if len(word) == 0:
        return state in dfa['F'], path

    if state not in dfa['delta'] or word[0] not in dfa['delta'][state]:
        return False, None

    input_symbol = word[0]
    new_state = dfa['delta'][state][input_symbol]
    new_path = path + [f"{state}-{input_symbol}"]
    return is_valid_word(dfa, word[1:], new_state, new_path)

# Gerar o grafo fo graphviz
def gerar_grafo(nome_arquivo, dfa):
    grafo = dfa['delta']

    with open(nome_arquivo + '.dot', 'w') as arquivo:
        arquivo.write('digraph ' + nome_arquivo + ' {\n')
        arquivo.write('\trankdir=LR;\n')
        arquivo.write('\tsize="8,5"\n')
        arquivo.write('\tnode [shape = doublecircle]; ' + ' '.join(dfa['F']) + '\n')
        arquivo.write('\tnode [shape = circle];\n')

        for origem, destinos in grafo.items():
            for destino, valor in destinos.items():
                arquivo.write(f'\t{origem} -> {valor} [ label = "{destino}" ];\n')

        arquivo.write('}\n')

    print("\nGraph file generated:", nome_arquivo + '.dot\n')

# Função principal que lê 
def main():
    if len(sys.argv) < 4:
        print("Usage: python afd_main.py AFD.json -rec <word>")
        return

    file_path = sys.argv[1]
    if sys.argv[2] != "-rec":
        print("Usage: python afd_main.py AFD.json -rec <word>")
        return

    word = sys.argv[3]

    dfa = load_dfa(file_path)
    gerar_grafo('grafo', dfa)  # Call gerar_grafo depois do AFD ser gerado

    num_states = len(dfa['Q'])

    if len(word) > num_states:
        print(f"The word '{word}' is not valid.")
        return
    elif len(word) == 1:
        initial_state = dfa['Q'][0]
        transition = dfa['delta'][initial_state]
        input_symbol = list(transition.keys())[0]
        if word == input_symbol:
            print(f"The word '{word}' is valid\n")
            print(f"{initial_state}-{word}")
            return
        else:
            print(f"The word '{word}' is not valid\n")
            return  

    valid, path = is_valid_word(dfa, word)

    if valid:
        print(f"The word '{word}' is valid.\n")
        # Imprimir caminho
        print("Path:", " -> ".join(path))
    else:
        print(f"The word '{word}' is not valid.\n")

if __name__ == "__main__":
    main()