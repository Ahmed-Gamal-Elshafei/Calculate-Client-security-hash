class Context:
    """Shared data and termination flag for the state machine."""

    def __init__(self):
        self.variables = {}  # Shared data between states
        self.terminate = False  # Flag to stop the state machine

    def stop(self):
        """Stop the state machine."""
        self.terminate = True
