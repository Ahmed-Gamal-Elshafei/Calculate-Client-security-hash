from automation.sha1.sha1_Read.Sha1_Output_Read import Sha1OutputRead
from automation.sha1.sha1_write.Sha1_Data_Write import Sha1DataWrite
from reusables.custom_exception import CustomException


def hash_data_init(driver, data_to_hash: str) -> str:
    """
    Initialize the SHA1 hashing process on the specified website.

    Args:
        driver: Selenium WebDriver instance.
        data_to_hash (str): The data string to be hashed.

    Returns:
        str: The hashed data retrieved from the website.

    Raises:
        CustomException: If writing data or reading the SHA1 hash fails.
    """
    function_name = "hash_data_sub_process"

    try:
        # Navigate to the SHA1 hash generator webpage
        url = "https://emn178.github.io/online-tools/sha1.html"
        driver.get(url)

        # Write data to the input field
        sha1_data_write = Sha1DataWrite(driver)
        sha1_data_write.start(data_to_hash)

        # Read the SHA1 hashed output
        sha1_output_read = Sha1OutputRead(driver)
        sha1_hashed_data: str = sha1_output_read.start()

        return sha1_hashed_data

    except (CustomException, Exception) as e:
        driver.get_screenshot_as_file(f'../Screenshots/{function_name}.png')
        driver.back()
        raise e
