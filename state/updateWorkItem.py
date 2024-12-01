from StateMachine import State
from sub_process.update_work_item_data import update_work_item_data
from reusables.custom_exception import CustomException


class UpdateWorkItem(State):
    """State responsible for updating work item data."""

    def execute(self, context):
        """Executes the work item update process."""
        try:
            print("Executing UpdateWorkItem State...")
            driver = context.variables["driver"]
            hashed_data = context.variables.get("hashed_data")

            # Attempt to update the work item using hashed data
            is_update = update_work_item_data(driver, hashed_data)
            original_window = driver.current_window_handle
            driver.close()
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break

            context.variables["is_update"] = is_update
            print(f"Work item updated: {is_update}")
            context.variables["status"] = "success"

        except (CustomException, Exception) as e:
            print(f"Error in UpdateWorkItem.execute: {e}")
            # context.terminate = True
            context.variables["status"] = "failed"

    def next_state(self, context):
        """Determines the next state based on the result of the work item update."""
        from state.pickItem import PickItem
        return PickItem()
