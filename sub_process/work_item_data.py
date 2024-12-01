from automation.work_item_page.work_item_page_navigate.Work_Item_Page_NavigateTo_Update_Page import \
    WorkItemPageNavigateToUpdatePage
from automation.work_item_page.work_item_page_read.Work_Item_Client_Data_Read import WorkItemClientDataRead
from reusables.custom_exception import CustomException


def work_item_data_init(driver, work_item_url: str) -> str:
    """
    Initialize work item data by navigating to the URL, reading data,
    and processing it for SHA1 hash generation.
    """
    function_name = "work_item_data_sub_process"
    try:
        driver.get(work_item_url)

        # Step 1: Read client data
        work_item_client_data_read = WorkItemClientDataRead(driver)
        client_data = work_item_client_data_read.start()

        # Step 2: Prepare data for SHA1 hash
        client_data = build_data_for_sha1(client_data)

        # Step 3: Navigate to update page
        work_item_page_navigate_to_update_page = WorkItemPageNavigateToUpdatePage(driver)
        work_item_page_navigate_to_update_page.start()

        # Handle window switching
        original_window = driver.current_window_handle
        driver_position = driver.get_window_position()
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                driver.set_window_position(driver_position['x'], driver_position['y'])
                break

        return client_data

    except (CustomException, Exception) as e:
        print(f"CustomException in {function_name}: {e}")
        driver.get_screenshot_as_file(f'../Screenshots/{function_name}.png')
        raise e  # Re-raise after logging


def build_data_for_sha1(client_data: str) -> str:
    """Builds a string for SHA1 hash from the client information."""
    client_id, client_name, client_country = "", "", ""
    client_info_lines = client_data.split("\n")

    for line in client_info_lines:
        if line.startswith("Client ID:"):
            client_id = line.replace("Client ID:", "").strip()
        elif line.startswith("Client Name:"):
            client_name = line.replace("Client Name:", "").strip()
        elif line.startswith("Client Country:"):
            client_country = line.replace("Client Country:", "").strip()

    return f"{client_id}-{client_name}-{client_country}"
