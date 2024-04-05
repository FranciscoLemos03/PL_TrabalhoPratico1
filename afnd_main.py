import json

class AFND:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def to_json(self):
        return {
            'states': list(self.states),
            'alphabet': list(self.alphabet),
            'transitions': {str(k): list(v) for k, v in self.transitions.items()},
            'initial_state': list(self.initial_state)[0],  # Convertendo de frozenset para lista e pegando o primeiro elemento
            'final_states': [list(state) for state in self.final_states]  # Convertendo frozenset para lista
        }

class AFD:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def to_json(self):
        return {
            'states': [list(state) for state in self.states],  # Convertendo frozenset para lista
            'alphabet': list(self.alphabet),
            'transitions': {str(k): list(v) for k, v in self.transitions.items()},
            'initial_state': list(self.initial_state)[0],  # Convertendo de frozenset para lista e pegando o primeiro elemento
            'final_states': [list(state) for state in self.final_states]  # Convertendo frozenset para lista
        }

def afnd_to_afd(afnd):
    queue = [frozenset([afnd.initial_state])]  # Inicia com o conjunto de estados iniciais do AFND
    visited = set()
    new_states = set()  # Conjunto de novos estados do AFD
    new_transitions = {}  # Transições do AFD
    final_states = set()

    while queue:
        current_states = queue.pop(0)
        if current_states in visited:
            continue
        visited.add(current_states)
        
        # Adiciona novo estado
        new_states.add(current_states)

        # Verifica se o estado atual é final
        if any(state in current_states for state in afnd.final_states):
            final_states.add(current_states)

        # Obtém transições para cada símbolo do alfabeto
        transitions = {}
        for symbol in afnd.alphabet:
            next_states = set()
            for state in current_states:
                next_states.update(afnd.transitions.get((state, symbol), []))
            
            if next_states:
                next_states_frozen = frozenset(next_states)
                transitions[(current_states, symbol)] = next_states_frozen
                
                # Se o próximo estado não estiver na lista de novos estados, adicione-o à fila
                if next_states_frozen not in new_states:
                    queue.append(next_states_frozen)

        new_transitions.update(transitions)

    return AFD(new_states, afnd.alphabet, new_transitions, frozenset([afnd.initial_state]), final_states)

def main():
    with open('AFND.json', 'r') as file:
        afnd_json = json.load(file)

    afnd = AFND(
        set(afnd_json['states']),
        set(afnd_json['alphabet']),
        {eval(k): v for k, v in afnd_json['transitions'].items()},  # Mantendo as chaves como estão
        frozenset([afnd_json['initial_state']]),
        set(frozenset(state) for state in afnd_json['final_states'])
    )

    afd = afnd_to_afd(afnd)

    with open('AFD.json', 'w') as file:
        json.dump(afd.to_json(), file, indent=4)

if __name__ == "__main__":
    main()