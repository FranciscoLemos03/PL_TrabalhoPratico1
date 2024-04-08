import json

class AFD:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    @classmethod
    def from_json(cls, filename):
        with open(filename, 'r') as file:
            afd_json = json.load(file)
        return cls(
        {tuple(state) for state in afd_json['states']},  # Convert inner lists to tuples
        set(afd_json['alphabet']),
        afd_json['transitions'],
        afd_json['initial_state'],
        {tuple(state) for state in afd_json['final_states']}  # Convert inner lists to tuples
    )


    def recognize_input(self, input_string):
        current_state = self.initial_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False  # Symbol not in alphabet, reject
            current_state = self.transitions.get(current_state, {}).get(symbol)
            if current_state is None:
                return False  # No transition defined, reject
        return current_state in self.final_states

def main():
    # Load AFD from JSON
    afd = AFD.from_json('AFD.json')

    # Get user input
    input_string = input("Enter a string: ")

    # Check if input is recognized by the AFD
    if afd.recognize_input(input_string):
        print("Input string is recognized by the AFD.")
    else:
        print("Input string is not recognized by the AFD.")

if __name__ == "__main__":
    main()
