import json

# Função que recebe o er.json e converte em afnd.json 
def construct_afnd(er_json):
    alphabet = set()
    states = set()
    transitions = {}
    final_states = set()

    state_counter = 0

    #gerar nome de estado
    def generate_state_name():
        nonlocal state_counter
        state_name = f"q{state_counter}"
        state_counter += 1
        return state_name

    # percorrer er.json e construir afnd
    def traverse(node, current_state):
        nonlocal alphabet, states, transitions, final_states

        if isinstance(node, dict):
            if "simb" in node:
                alphabet.add(node["simb"])
                return

            if "op" in node:
                if node["op"] == "alt":
                    left_state = generate_state_name()
                    right_state = generate_state_name()
                    states.add(left_state)
                    states.add(right_state)

                    traverse(node["args"][0], left_state)
                    traverse(node["args"][1], right_state)

                    transitions[current_state] = {
                        "": [left_state, right_state]
                    }

                elif node["op"] == "seq":
                    prev_state = current_state
                    for idx, arg in enumerate(node["args"]):
                        new_state = generate_state_name()
                        states.add(new_state)
                        traverse(arg, new_state)
                        #Verificar que o valor da transição é sempre lista
                        if arg.get("simb"):
                            transitions.setdefault(prev_state, {}).setdefault(arg["simb"], []).append(new_state)
                        else:
                            transitions.setdefault(prev_state, {}).setdefault("", []).append(new_state)
                        prev_state = new_state
                    final_states.add(new_state)

                elif node["op"] == "kle":
                    new_state = generate_state_name()
                    states.add(new_state)
                    transitions[current_state] = {node["args"][0].get("simb", ""): new_state}
                    transitions[new_state] = {node["args"][0].get("simb", ""): new_state}
                    final_states.add(new_state)
                    traverse(node["args"][0], new_state)

    initial_state = "q0"
    states.add(initial_state)
    traverse(er_json, initial_state)

    return {
        "V": sorted(list(alphabet)),  #Sort alfabeto
        "Q": sorted(list(states)),
        "delta": transitions,
        "q0": initial_state,
        "F": sorted(list(final_states))
    }

def read_er_from_file(file_path):
    with open(file_path, "r") as file:
        er_json = json.load(file)
    return er_json

er_json = read_er_from_file("ER.json")

afnd_json = construct_afnd(er_json)

#Escrever o AFND é um ficheiro json .json
with open("AFND.json", "w") as afnd_file:
    json.dump(afnd_json, afnd_file, indent=4)

print("Estrutura AFND JSON foi salva no ficheiro AFND.json.")