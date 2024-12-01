from StateMachine import StateMachine
from context import Context
from state.initializeVariable import InitializeVariable
from reusables.recorder import stop_recording

import sys

if __name__ == "__main__":
    # Initialize the context and state machine
    context = Context()
    initial_state = InitializeVariable()
    state_machine = StateMachine(initial_state, context)

    # Run the state machine
    state_machine.run()
    print("State machine execution completed.")
    stop_recording()
    sys.exit(0)
