import json

class AFND:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def to_json(self):
        delta = {state: {symbol: self.transitions.get((state, symbol), []) for symbol in sorted(self.alphabet)} for state in sorted(self.states)}

        return {
            "V": sorted(list(self.alphabet)),
            "Q": sorted(list(self.states)),
            "delta": delta,
            "q0": self.initial_state,
            "F": sorted(list(self.final_states))
        }


def parse_json_to_afnd(json_data):
    if 'op' in json_data:
        if json_data['op'] == 'alt':
            # Se a operação for uma alternância (alt), precisamos criar um AFND para cada argumento
            afnd1 = parse_json_to_afnd(json_data['args'][0])
            afnd2 = parse_json_to_afnd(json_data['args'][1])
            
            # Unir os AFNDs
            new_states = afnd1.states.union(afnd2.states)
            new_states.add('q0')  # Adicionar novo estado inicial
            new_states.add('qf')  # Adicionar novo estado final
    
            new_transitions = afnd1.transitions.copy()
            new_transitions.update(afnd2.transitions)
            
            # Adicionar transição vazia do novo estado inicial para os antigos estados iniciais dos AFNDs
            new_transitions[('q0', '')] = [afnd1.initial_state, afnd2.initial_state]
            
            # Adicionar transição vazia dos antigos estados finais dos AFNDs para o novo estado final
            for state in afnd1.final_states:
                new_transitions[('',)].append(state)
            for state in afnd2.final_states:
                new_transitions[('',)].append(state)
    
            return AFND(new_states, afnd1.alphabet.union(afnd2.alphabet), new_transitions, 'q0', {'qf'})
        
        elif json_data['op'] == 'seq':
            # Se a operação for uma sequência (seq), precisamos criar um AFND para cada argumento e concatená-los
            afnd1 = parse_json_to_afnd(json_data['args'][0])
            afnd2 = parse_json_to_afnd(json_data['args'][1])
    
            new_states = afnd1.states.union(afnd2.states)
            new_transitions = afnd1.transitions.copy()
            new_transitions.update(afnd2.transitions)
    
            # Adicionar transição vazia dos antigos estados finais de afnd1 para o estado inicial de afnd2
            for state in afnd1.final_states:
                new_transitions[('',)].append(afnd2.initial_state)
    
            return AFND(new_states, afnd1.alphabet.union(afnd2.alphabet), new_transitions, afnd1.initial_state, afnd2.final_states)
        
        elif json_data['op'] == 'kle':
            # Se a operação for uma estrela de Kleene (kle), precisamos criar um AFND para o argumento e aplicar a estrela de Kleene
            afnd = parse_json_to_afnd(json_data['args'][0])
            
            new_states = afnd.states
            new_states.add('q0')  # Adicionar novo estado inicial
            new_states.add('qf')  # Adicionar novo estado final
    
            new_transitions = afnd.transitions.copy()
    
            # Adicionar transições vazias do novo estado inicial para os antigos estados iniciais e finais do AFND
            new_transitions[('q0', '')] = [afnd.initial_state]
            new_transitions[('',)] = list(afnd.final_states) + [afnd.initial_state, 'qf']
            
            return AFND(new_states, afnd.alphabet, new_transitions, 'q0', {'qf'})
    elif 'simb' in json_data:
        # Se o nó tiver um símbolo, este é um estado simples
        states = {'q0', 'q1'}
        transitions = {('q0', json_data['simb']): ['q1']}
        return AFND(states, {json_data['simb']}, transitions, 'q0', {'q1'})
    else:
        raise ValueError("Operação inválida")

def main():
    with open('er.json', 'r') as file:
        json_data = json.load(file)

    afnd = parse_json_to_afnd(json_data)

    with open('AFND.json', 'w') as file:
        json.dump(afnd.to_json(), file, indent=4)

if __name__ == "__main__":
    main()
