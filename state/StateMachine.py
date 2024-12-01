class State:
    """Abstract base class for states."""

    def execute(self, context):
        """Perform the action for this state."""
        raise NotImplementedError("Subclasses must implement this method.")

    def next_state(self, context):
        """Determine the next state."""
        return None


class StateMachine:
    """State Machine to execute states sequentially."""

    def __init__(self, initial_state, context):
        if not initial_state or not hasattr(initial_state, "execute"):
            raise ValueError("Initial state must implement the 'execute' method.")
        self.current_state = initial_state
        self.context = context

    def run(self):
        """Run the state machine until termination or no next state."""
        try:
            while self.current_state and not self.context.terminate:
                self.current_state.execute(self.context)
                self.current_state = self.current_state.next_state(self.context)
        except Exception as e:
            print(f"StateMachine encountered an error: {e}")

