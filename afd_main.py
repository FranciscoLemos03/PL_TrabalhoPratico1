import graphviz  # doctest: +NO_EXE
import json
import ast
import sys

import json
import ast
import sys

class AFD:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

def load_afd_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        afd_data = json.load(f)

    # Flatten the states from nested lists to a single set
    states = set()
    for state_list in afd_data["states"]:
        states.update(state_list)

    # Convert transitions keys directly to strings
    transitions = {}
    for key, value in afd_data["transitions"].items():
        transitions[key] = value

    return AFD(
        states=states,
        alphabet=set(afd_data["alphabet"]),
        transitions=transitions,
        initial_state=afd_data["initial_state"],
        final_states=set(afd_data["final_states"])
    )


def verifica_afd(afd):
    # Verificar se os campos obrigatórios estão presentes
    campos_obrigatorios = ["states", "alphabet", "transitions", "initial_state", "final_states"]
    for campo in campos_obrigatorios:
        if not hasattr(afd, campo):
            print(f"Falta o campo obrigatório '{campo}'", file=sys.stderr)
            return False
    
    # Verificar se o conjunto de estados finais está contido no conjunto de estados
    if not afd.final_states.issubset(afd.states):
        print("Conjunto de estados finais não está contido no conjunto de estados", file=sys.stderr)
        return False
    
    # Verificar se a função de transição está bem definida
    for estado, transicoes in afd.transitions.items():
        if estado not in afd.states:
            print(f"Estado '{estado}' nas transições não está no conjunto de estados", file=sys.stderr)
            return False
        for simbolo, destino in transicoes.items():
            if simbolo not in afd.alphabet:
                print(f"Símbolo '{simbolo}' nas transições não está no alfabeto", file=sys.stderr)
                return False
            if destino not in afd.states:
                print(f"Destino '{destino}' nas transições não está no conjunto de estados", file=sys.stderr)
                return False
    
    print("Autômato está corretamente estruturado de acordo com as regras de um AFD")
    return True

# Load AFD from file
try:
    af = load_afd_from_file('AFD.json')
    verifica_afd(af)
except Exception as e:
    print(f"Error loading AFD from file: {e}", file=sys.stderr)





# Verificar se o autômato está corretamente estruturado


def gerar_grafo(nome_arquivo, afd):
    grafo = afd.transitions

    with open(nome_arquivo + '.dot', 'w') as arquivo:
        arquivo.write('digraph ' + nome_arquivo + ' {\n')
        arquivo.write('\trankdir=LR;\n')
        arquivo.write('\tsize="8,5"\n')
        arquivo.write('\tnode [shape = doublecircle]; ' + ' '.join(afd.final_states) + ';\n')
        arquivo.write('\tnode [shape = circle];\n')

        for origem, destinos in grafo.items():
            for destino, valor in destinos.items():
                arquivo.write(f'\t{origem} -> {valor} [ label = "{destino}" ];\n')

        arquivo.write('}\n')


gerar_grafo('grafo', af)
