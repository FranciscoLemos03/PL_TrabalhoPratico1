import json

#Função que recebe o afnd.json e converte em afd.json 
def epsilon_closure(states, delta):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        if "" in delta.get(state, {}):
            new_states = delta[state][""]
            for new_state in new_states:
                if new_state not in closure:
                    closure.add(new_state)
                    stack.append(new_state)
    return closure

def move(states, symbol, delta):
    result = set()
    for state in states:
        transitions = delta.get(state, {})
        if symbol in transitions:
            result.update(transitions[symbol])
    return result


def nfa_to_dfa(nfa):
    V = nfa["V"]
    Q = []
    delta = {}
    q0 = nfa["q0"]
    F = []
    queue = [epsilon_closure([q0], nfa["delta"])]
    dfa_states_map = {}
    dfa_states_map[frozenset(queue[0])] = "q0"
    while queue:
        current_states = queue.pop(0)
        current_dfa_state = dfa_states_map[frozenset(current_states)]
        Q.append(current_dfa_state)
        for symbol in V:
            next_states = epsilon_closure(move(current_states, symbol, nfa["delta"]), nfa["delta"])
            if next_states:
                if frozenset(next_states) not in dfa_states_map:
                    queue.append(next_states)
                    dfa_states_map[frozenset(next_states)] = "q" + str(len(dfa_states_map))
                delta.setdefault(current_dfa_state, {})
                delta[current_dfa_state][symbol] = dfa_states_map[frozenset(next_states)]
        if any(state in nfa["F"] for state in current_states):
            F.append(current_dfa_state)
    return {"V": V, "Q": Q, "delta": delta, "q0": q0, "F": F}


def main():
    # Ler AFND do JSON file
    with open("AFND.json", "r") as f:
        nfa = json.load(f)

    # converter AFND para AFD
    dfa = nfa_to_dfa(nfa)

    #Estrutura de AFD
    formatted_dfa = {
        "V": list(nfa["V"]),
        "Q": [f"q{i}" for i in range(len(dfa["Q"]))],
        "delta": {state: {symbol: target_state for symbol, target_state in transitions.items() if ',' not in target_state and target_state.strip() != ""} for state, transitions in nfa["delta"].items() if ',' not in state},
        "q0": dfa["q0"],
        "F": [state for state in dfa["Q"] if any(substate in nfa["F"] for substate in state.split(","))]
    }

    #Salvar a estrutura no ficheiro AFD.json
    with open("AFD.json", "w") as f:
        json.dump(formatted_dfa, f, indent=4)

    
    print("Estrutura AFD JSON foi salva no ficheiro AFD.json.")


if __name__ == "__main__":
    main()
