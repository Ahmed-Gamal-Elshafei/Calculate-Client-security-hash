from reusables.custom_exception import CustomException
from state.StateMachine import State
from sub_process.login_acme import login_init


class Login(State):
    """State to perform login operations."""

    def execute(self, context):
        """Execute login using provided credentials."""
        try:
            print("Executing Login State...")

            # Retrieve login credentials
            credentials = context.variables.get("credentials", {}).get("login_credentials", {})
            if not credentials:
                raise ValueError("Login credentials are missing from the context variables.")

            user_name = credentials.get("username")
            password = credentials.get("password")
            if not user_name or not password:
                raise ValueError("Username or password is missing in the login credentials.")

            print(f"Attempting to log in with username: {user_name}")

            # Perform the login operation
            login_success = login_init(context.variables["driver"], user_name, password)

            if not login_success:
                raise RuntimeError("Login failed. Please check the credentials or driver.")
            print("Login successful.")

        except (CustomException, Exception) as e:
            print(f"Error in Login by selenium library: {e}")
            context.variables["driver"].quit()
            context.terminate = True

    def next_state(self, context):
        """Proceed to the PickItem state."""
        from state.pickItem import PickItem
        return PickItem()
