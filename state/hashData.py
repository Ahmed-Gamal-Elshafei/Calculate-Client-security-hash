from StateMachine import State
from sub_process.hash_data import hash_data_init
from reusables.custom_exception import CustomException


class HashData(State):
    """State responsible for handling the hash data processing."""

    def execute(self, context):
        """Executes the data hashing process."""
        try:
            print("Executing HashData State...")
            driver = context.variables["driver"]
            client_data = context.variables.get("client_data")

            if not client_data:
                raise CustomException("No client data available for hashing.")

            hashed_data = hash_data_init(driver, client_data)
            context.variables["hashed_data"] = hashed_data

            print("Hashed data:", hashed_data)
            driver.back()  # Navigate back after processing the hash

        except (CustomException, Exception) as e:
            print(f"Error in HashData.execute: {e}")
            # context.terminate = True
            context.variables["status"] = "failed"

    def next_state(self, context):
        """Determines the next state based on the result of the hashing process."""
        if context.variables.get("hashed_data"):
            print("Hashed data found, proceeding to UpdateWorkItem state.")
            from state.updateWorkItem import UpdateWorkItem
            return UpdateWorkItem()
        else:
            print("No hashed data found, terminating process.")
            context.variables["driver"].quit()
            context.variables["status"] = "failed"
            # return to pick item to update the status of item it xlsx file
            from state.pickItem import PickItem
            return PickItem()
            # context.terminate = True
            # return None
