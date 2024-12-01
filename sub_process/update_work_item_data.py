from automation.work_item_update_page.work_item_update__page_navigate.Work_Item_Update_Page_Confirm_Form import \
    WorkItemUpdatePageConfirmForm
from automation.work_item_update_page.work_item_update_page_select.Work_Item_Update_page_Select import \
    WorkItemUpdatePageSelect
from automation.work_item_update_page.work_item_update_page_write.Work_Item_Update_page_Write import \
    WorkItemUpdatePageWrite

from reusables.custom_exception import CustomException


def update_work_item_data(driver, client_data: str) -> bool:
    function_name = "update_work_item_data_sub_process"
    try:
        # Write the updated work item data
        work_item_update_page_write = WorkItemUpdatePageWrite(driver)
        work_item_update_page_write.start(client_data)

        # Select the appropriate work item update options
        work_item_update_page_select = WorkItemUpdatePageSelect(driver)
        work_item_update_page_select.start()

        # Confirm the update
        work_item_update_page_confirm_form = WorkItemUpdatePageConfirmForm(driver)
        _is_success = work_item_update_page_confirm_form.start()

        return _is_success
    except CustomException as e:
        print(f"Error in {function_name}: {e}")
        driver.get_screenshot_as_file(f'../Screenshots/{function_name}.png')
        raise e  # Re-raise the exception after logging it
