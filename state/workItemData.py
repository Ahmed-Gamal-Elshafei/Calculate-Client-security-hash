from StateMachine import State

from reusables.custom_exception import CustomException
from sub_process.work_item_data import work_item_data_init


class WorkItemData(State):
    """State to handle work item data processing."""

    def execute(self, context):
        """Executes the work item data retrieval and processes it."""
        try:
            print("Executing WorkItemData State...")
            driver = context.variables["driver"]
            work_item = context.variables["item"]
            # print("Work Item:", work_item)
            client_data = work_item_data_init(driver, work_item["item"]["Url"])
            context.variables["client_data"] = client_data
        except (CustomException, Exception) as e:
            print(f"Error in WorkItemData.execute: {e}")
            # context.terminate = True
            context.variables["status"] = "failed"

    def next_state(self, context):
        """Determines the next state based on client data availability."""
        if context.variables.get("client_data"):
            print("Client data found, proceeding to HashData state.")
            from state.hashData import HashData
            return HashData()
        else:
            print("No client data found, terminating process.")
            context.variables["driver"].quit()
            context.variables["status"] = "failed"
            # return to pick item to update the status of item it xlsx file
            from state.pickItem import PickItem
            return PickItem()
