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
            # Use the string representation of the state as key
            state_str = key
            transitions_dict[state_str] = value
        return {
        'states': list(self.states),  # Extract the state names
        'alphabet': list(self.alphabet),
        'transitions': transitions_dict,
        'initial_state': self.initial_state,  # Extract the initial state name
        'final_states': list(self.final_states)  # Extract the final state names
    }






def afnd_to_afd(afnd):
    queue = [frozenset([afnd.initial_state])]
    visited = set()
    new_states = set()
    new_transitions = {}
    final_states = set()

    while queue:
        current_states = queue.pop(0)
        if current_states in visited:
            continue
        visited.add(current_states)

        new_states.add(tuple(current_states))  # Convert frozenset to tuple

        if any(state in current_states for state in afnd.final_states):
            final_states.add(tuple(current_states))  # Convert frozenset to tuple

        transitions = {}
        for symbol in afnd.alphabet:
            next_states = set()
            for state in current_states:
                next_states.update(afnd.transitions.get((state, symbol), []))
            if next_states:
                next_states_frozen = frozenset(next_states)
                if next_states_frozen not in new_states:
                    queue.append(next_states_frozen)
                transitions[symbol] = [s.split(',')[1] if ',' in s else s for s in next_states]

        # Convert frozenset of states to a tuple representation
        current_states_tuple = tuple(sorted([s.split(',')[1] if ',' in s else s for s in current_states]))
        new_transitions[current_states_tuple] = transitions  # Use the tuple as the key

    # Convert transitions to a more conventional representation
    afd_transitions = {}
    for source_states, transition in new_transitions.items():
        destination_states_map = {}
        for symbol, destination_states in transition.items():
            # Convert list of states to string representation
            destination_states_str = ','.join(destination_states)
            destination_states_map[symbol] = destination_states_str
        # Convert tuple of states to a string representation
        source_states_str = ','.join(sorted([s.split(',')[1] if ',' in s else s for s in source_states]))
        afd_transitions[source_states_str] = destination_states_map

    return AFD(new_states, afnd.alphabet, afd_transitions, afnd.initial_state, final_states)










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

    # Save AFD to JSON
    with open('AFD.json', 'w') as file:
        json.dump(afd.to_dict(), file, indent=4)

if __name__ == "__main__":
    main()
