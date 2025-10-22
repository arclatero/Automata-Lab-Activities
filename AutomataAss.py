class State:
    """Represents a state in a state machine"""
    def __init__(self, name, output=None):
        self.name = name
        self.output = output  # For Moore machine (output associated with state)
        self.transitions = {}  # Dictionary to store transitions
    
    def add_transition(self, input_symbol, next_state, output=None):
        """Add a transition from this state"""
        self.transitions[input_symbol] = {'next_state': next_state, 'output': output}
    
    def get_transition(self, input_symbol):
        """Get the transition information based on input symbol"""
        return self.transitions.get(input_symbol, None)


class MooreMachine:
    """Moore Machine implementation - Output depends on STATE only"""
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.start_state = None
    
    def add_state(self, name, output, is_start=False):
        """Add a state to the machine"""
        state = State(name, output)
        self.states[name] = state
        
        if is_start:
            self.start_state = state
            self.current_state = state
        
        return state
    
    def add_transition(self, from_state, input_symbol, to_state):
        """Add a transition between states"""
        if from_state in self.states and to_state in self.states:
            self.states[from_state].add_transition(
                input_symbol, 
                self.states[to_state]
            )
    
    def reset(self):
        """Reset the machine to start state"""
        self.current_state = self.start_state
    
    def process_input(self, input_string):
        """Process an input string and generate output"""
        self.reset()
        outputs = []
        
        print(f"\nProcessing input: {input_string}")
        print(f"Initial State: {self.current_state.name}, Output: '{self.current_state.output}'")
        print("-" * 60)
        
        for i, symbol in enumerate(input_string):
            # MOORE: Output comes from current state
            output = self.current_state.output
            outputs.append(output)
            
            # Transition to next state
            transition = self.current_state.get_transition(symbol)
            if transition:
                next_state = transition['next_state']
                print(f"Step {i+1}: Input='{symbol}' | State={self.current_state.name} | "
                      f"Output='{output}' | Next State={next_state.name}")
                self.current_state = next_state
        
        # Output for final state
        final_output = self.current_state.output
        outputs.append(final_output)
        print(f"\nFinal State: {self.current_state.name}, Final Output: '{final_output}'")
        print("-" * 60)
        
        return ''.join(outputs)


class MealyMachine:
    """Mealy Machine implementation - Output depends on STATE and INPUT (transition)"""
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.start_state = None
    
    def add_state(self, name, is_start=False):
        """Add a state to the machine (no output on state in Mealy)"""
        state = State(name)
        self.states[name] = state
        
        if is_start:
            self.start_state = state
            self.current_state = state
        
        return state
    
    def add_transition(self, from_state, input_symbol, to_state, output):
        """Add a transition with output between states"""
        if from_state in self.states and to_state in self.states:
            self.states[from_state].add_transition(
                input_symbol, 
                self.states[to_state],
                output
            )
    
    def reset(self):
        """Reset the machine to start state"""
        self.current_state = self.start_state
    
    def process_input(self, input_string):
        """Process an input string and generate output"""
        self.reset()
        outputs = []
        
        print(f"\nProcessing input: {input_string}")
        print(f"Initial State: {self.current_state.name}")
        print("-" * 60)
        
        for i, symbol in enumerate(input_string):
            # MEALY: Output comes from transition (state + input)
            transition = self.current_state.get_transition(symbol)
            if transition:
                output = transition['output']
                next_state = transition['next_state']
                outputs.append(output)
                
                print(f"Step {i+1}: State={self.current_state.name} | Input='{symbol}' | "
                      f"Output='{output}' | Next State={next_state.name}")
                self.current_state = next_state
        
        print(f"\nFinal State: {self.current_state.name}")
        print("-" * 60)
        
        return ''.join(outputs)


def create_moore_machine():
    """
    Moore Machine: Output 'a' when '01' is detected, otherwise 'b'
    Output depends on STATE only
    
    States:
    - A: Start state - output: 'b'
    - B: Saw '0' - output: 'b'
    - C: Detected '01' - output: 'a'
    """
    machine = MooreMachine()
    
    machine.add_state('A', 'b', is_start=True)
    machine.add_state('B', 'b')
    machine.add_state('C', 'a')
    
    # Transitions
    machine.add_transition('A', '0', 'B')
    machine.add_transition('A', '1', 'A')
    machine.add_transition('B', '0', 'B')
    machine.add_transition('B', '1', 'C')
    machine.add_transition('C', '0', 'B')
    machine.add_transition('C', '1', 'A')
    
    return machine


def create_mealy_machine():
    """
    Mealy Machine: Output 'a' when '01' is detected, otherwise 'b'
    Output depends on STATE and INPUT (transition)
    
    States:
    - A: Start state
    - B: Saw '0'
    - C: Continue after detecting '01'
    """
    machine = MealyMachine()
    
    machine.add_state('A', is_start=True)
    machine.add_state('B')
    machine.add_state('C')
    
    # Transitions with outputs (input/output on each transition)
    machine.add_transition('A', '0', 'B', 'b')  # A --0/b--> B
    machine.add_transition('A', '1', 'A', 'b')  # A --1/b--> A
    machine.add_transition('B', '0', 'B', 'b')  # B --0/b--> B
    machine.add_transition('B', '1', 'C', 'a')  # B --1/a--> C (detected '01'!)
    machine.add_transition('C', '0', 'B', 'b')  # C --0/b--> B
    machine.add_transition('C', '1', 'A', 'b')  # C --1/b--> A
    
    return machine


def validate_input(input_string):
    """Validate if input contains only 0s and 1s"""
    for char in input_string:
        if char not in ['0', '1']:
            return False
    return True


# Main execution
if __name__ == "__main__":
    print("=" * 70)
    print("MOORE vs MEALY MACHINES: Detecting '01' sequence")
    print("=" * 70)
    print("\nKEY DIFFERENCES:")
    print("- MOORE: Output depends on STATE only")
    print("- MEALY: Output depends on STATE + INPUT (transition)")
    print("=" * 70)
    
    # Create both machines
    moore = create_moore_machine()
    mealy = create_mealy_machine()
    
    # Test cases
    test_inputs = ["01", "0101", "11", "00110"]
    
    for test_input in test_inputs:
        print("\n" + "=" * 70)
        print(f"Testing input: '{test_input}'")
        print("=" * 70)
        
        print("\n--- MOORE MACHINE ---")
        moore_output = moore.process_input(test_input)
        print(f"Moore Result: '{moore_output}'")
        
        print("\n--- MEALY MACHINE ---")
        mealy_output = mealy.process_input(test_input)
        print(f"Mealy Result: '{mealy_output}'")
        
        print(f"\n✓ '01' detected: Moore={moore_output.count('a')} times, "
              f"Mealy={mealy_output.count('a')} times")
    
    # User input section
    print("\n" + "=" * 70)
    print("USER INPUT SECTION")
    print("=" * 70)
    
    while True:
        user_input = input("\nEnter a binary string (or 'quit'): ").strip()
        
        if user_input.lower() == 'quit':
            print("\nThank you!")
            break
        
        if not user_input or not validate_input(user_input):
            print("⚠ Invalid input! Use only 0s and 1s.")
            continue
        
        print("\n--- MOORE MACHINE ---")
        moore_output = moore.process_input(user_input)
        print(f"Result: '{moore_output}'")
        
        print("\n--- MEALY MACHINE ---")
        mealy_output = mealy.process_input(user_input)
        print(f"Result: '{mealy_output}'")