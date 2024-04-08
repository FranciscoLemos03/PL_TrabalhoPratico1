import json

class AFND:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

class AFD:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def to_dict(self):
        transitions_dict = {}
        for key, value in self.transitions.items():
            state_list = list(key)
            value_dict = {}
            for symbol, destination in value.items():
                value_dict[symbol] = list(destination)
            transitions_dict[state_list[0]] = value_dict
        return {
            'states': [list(state) for state in self.states],
            'alphabet': list(self.alphabet),
            'transitions': transitions_dict,
            'initial_state': list(self.initial_state)[0],
            'final_states': [list(state) for state in self.final_states]
        }

class FrozenSetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, frozenset):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def afnd_to_afd(afnd):
    queue = [frozenset([afnd.initial_state])]
    visited = set()
    new_states = set()
    new_transitions = {}
    final_states = set()  # Create an empty set for final states

    while queue:
        current_states = queue.pop(0)
        if current_states in visited:
            continue
        visited.add(current_states)

        new_states.add(current_states)

        transitions = {}
        for symbol in afnd.alphabet:
            next_states = set()
            for state in current_states:
                next_states.update(afnd.transitions.get((state, symbol), []))
                next_states.update(afnd.transitions.get((state, ''), []))
            if next_states:
                next_states_frozen = frozenset(next_states)
                if next_states_frozen not in new_states:
                    queue.append(next_states_frozen)
                transitions[symbol] = next_states_frozen

        new_transitions[current_states] = transitions

        # Check if any state in current_states contains a final state
        for state in current_states:
            if state in afnd.final_states:
                final_states.add(current_states)
                break

    return AFD(new_states, afnd.alphabet, new_transitions, frozenset([afnd.initial_state]), final_states)







def main():
    # Load AFND from JSON
    with open('AFND.json', 'r') as file:
        afnd_json = json.load(file)

    afnd = AFND(
        set(afnd_json['states']),
        set(afnd_json['alphabet']),
        {eval(k): v for k, v in afnd_json['transitions'].items()},
        afnd_json['initial_state'],
        set(afnd_json['final_states'])
    )

    # Convert AFND to AFD
    afd = afnd_to_afd(afnd)

    # Save AFD to JSON with custom encoder
    with open('AFD.json', 'w') as file:
        json.dump(afd.to_dict(), file, indent=4, cls=FrozenSetEncoder)

if __name__ == "__main__":
    main()
