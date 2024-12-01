from StateMachine import State
from reusables.custom_exception import CustomException

from sub_process.pick_item import get_item, update_item, check_item_bot


class PickItem(State):
    """State to pick and process an item."""

    def execute(self, context):
        """Executes item picking, updates its status, and recycles if needed."""
        try:
            print("Executing PickItem State...")
            status = context.variables.get("status", None)

            # If item was updated, update the status and check for the next item
            if status == "success":
                print("Item updated.")
                self._update_item_status(context, {"_status": "success", "Status": "Complete", "lock": False})
                # Check again for a new item after the update
                self._pick_new_item(context)
            elif status == "failed":
                print("Item update failed.")
                __item = context.variables.get("item")
                __item = __item["item"]
                self._update_item_status(context,
                                         {"_status": "fail",
                                          "retry_number": __item["retry_number"] + 1, "lock": False})
                # Check again for a new item after the update
                self._pick_new_item(context)
            else:
                # If no item was updated, pick a new one
                self._pick_new_item(context)

        except (CustomException, Exception) as e:
            print(f"Error in PickItem.execute: {e}")
            context.terminate = True

    def next_state(self, context):
        """Determines the next state based on item availability."""
        if context.variables.get("item"):
            print("Item found, proceeding to WorkItemData state.")
            from state.workItemData import WorkItemData
            return WorkItemData()
        else:
            print("No item found, terminating process.")
            context.variables["driver"].quit()
            context.terminate = True
            return None

    @staticmethod
    def _pick_new_item(context):
        """Retrieves a new item and updates context variables."""
        bot_id = context.variables["bot_id"]
        item, row_idx = get_item(bot_id)

        if item:
            if check_item_bot(bot_id, row_idx):
                print(f"Item picked: {item}")
                context.variables["item"] = {"item": item, "row_idx": row_idx}
            else:
                PickItem._pick_new_item(context)
        else:
            print("No suitable item found.")

    @staticmethod
    def check_item_bot(bot_id):

        return True

    @staticmethod
    def _update_item_status(context, updated_values):
        """Updates the status of the current item."""
        item_row_idx = context.variables.get("item", {}).get("row_idx")
        if item_row_idx is not None:
            update_item(item_row_idx, updated_values)
            context.variables["item"] = None
