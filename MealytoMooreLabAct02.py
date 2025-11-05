class MooreMachine:
    def __init__(self):
        # States: format is 'StateName/Output'
        # Transitions map: state -> {input -> next_state}
        self.transitions = {
            'A/A': {'0': 'A/A', '1': 'B/B'},
            'B/B': {'0': 'C/A', '1': 'D/B'},
            'C/A': {'0': 'D/C', '1': 'B/B'},
            'D/B': {'0': 'B/B', '1': 'E/C'},
            'D/C': {'0': 'B/B', '1': 'C/C'},
            'E/C': {'0': 'D/C', '1': 'E/C'},
            'C/C': {'0': 'D/C', '1': 'B/B'}
        }
        
        # Extract output from state name (part after '/')
        self.start_state = 'A/A'
    
    def get_output(self, state):
        """Extract output from state name"""
        return state.split('/')[1]
    
    def process_input(self, input_string):
        """
        Process input string and return output string
        In Moore machines, output depends only on current state
        """
        current_state = self.start_state
        output = []
        
        # Add initial state output
        output.append(self.get_output(current_state))
        
        print(f"Initial state: {current_state}, Output: {self.get_output(current_state)}")
        
        for symbol in input_string:
            if symbol not in ['0', '1']:
                print(f"Invalid input symbol: {symbol}")
                continue
            
            # Get next state based on input
            next_state = self.transitions[current_state][symbol]
            
            # Get output from next state (Moore machine property)
            state_output = self.get_output(next_state)
            output.append(state_output)
            
            print(f"Input: {symbol}, Current: {current_state}, Next: {next_state}, Output: {state_output}")
            
            # Update current state
            current_state = next_state
        
        return ''.join(output)


def main():
    # Create Moore Machine
    moore = MooreMachine()
    
    # Test inputs
    test_inputs = ['00110', '11001', '1010110', '101111']
    
    print("=" * 60)
    print("MOORE MACHINE - INPUT/OUTPUT PROCESSING")
    print("=" * 60)
    
    # Process default test inputs
    print("\n📋 Processing default test inputs:")
    for input_str in test_inputs:
        print(f"\n--- Processing Input: {input_str} ---")
        output = moore.process_input(input_str)
        print(f"\nInput:  {input_str}")
        print(f"Output: {output}")
        print("-" * 60)
    
    # Interactive mode
    print("\n" + "=" * 60)
    print("🔄 INTERACTIVE MODE - Test Your Own Inputs")
    print("=" * 60)
    
    while True:
        print("\n")
        user_input = input("Enter a binary string (0s and 1s only) or 'exit' to quit: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Thank you for using the Moore Machine! Goodbye!")
            break
        
        # Validate input
        if not user_input:
            print("⚠️  Error: Please enter a valid binary string!")
            continue
        
        if not all(c in '01' for c in user_input):
            print("⚠️  Error: Input must contain only 0s and 1s!")
            continue
        
        # Process the input
        print(f"\n--- Processing Input: {user_input} ---")
        output = moore.process_input(user_input)
        print(f"\n✅ Input:  {user_input}")
        print(f"✅ Output: {output}")
        print("-" * 60)


if __name__ == "__main__":
    main()