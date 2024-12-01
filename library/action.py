"""
Action class for performing actions on the web page.

This module provides a class for performing actions on the web page, such as
clicking on an element, sending keys to an input field, and waiting for an
element to be present in the DOM.
"""

import time
import logging
import threading
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from library.constants import ClickButton, ClickType, Timeout
from reusables import logging_config

logger = logging.getLogger(__name__)


class Action:
    """
    Action class for performing actions on the web page.
    """
    HIGHLIGHT_DURATION = 0.3  # Constant for highlight duration
    DEBUG_MODE = True  # Enable or disable debug mode globally

    def __init__(self, driver: webdriver):
        self.driver = driver
        self.result_found = None  # Shared variable to store found element
        self.found_event = threading.Event()
        self.lock = threading.Lock()  # Lock for thread-safe access

    def _wait_for_element(self, timeout: Timeout) -> WebDriverWait:
        """Wait for an element to be present in the DOM."""
        wait = WebDriverWait(self.driver, timeout.value, poll_frequency=0.5)
        return wait

    def Click(
            self,
            name,
            selector,
            timeout: Timeout = Timeout.MEDIUM,
            click_type=ClickType.SINGLE,
            click_button=ClickButton.LEFT,
            delay_before=0,
            delay_after=0,
    ):
        """
        Perform the click action.

        Args:
            name (str): name of action
            selector (str): selector of the element
            timeout (int): timeout in seconds
            click_type (ClickType): click type
            click_button (ClickButton): click button
            delay_before (int): delay before the click in milliseconds
            delay_after (int): delay after the click in milliseconds

        Returns:
            bool: True if the click action was successful, False otherwise
        """
        logger.info(f"Enter Click from {name} ...")
        # delay before the click
        self._waitBeforeAction(delay_before)
        wait = self._wait_for_element(timeout)
        # wait for the element to be clickable
        element: WebElement = wait.until(
            EC.element_to_be_clickable((By.XPATH, selector))
        )
        # perform the click
        # check click and button type
        match click_button:
            case ClickButton.LEFT:
                self._HighlightElement(element)
                element.click()
                # logger.info(f"Clicked on {selector}")

        logger.info(f"Exit Click from {name} ...")
        # delay after the click
        self._waitBeforeAction(delay_after)
        return True

    def IsExist(self, name, selector, timeout: Timeout = Timeout.LONG):
        """
        Check if the element exists.

        Args:
            name (str): name of action
            selector (str): selector of the element
            timeout (int): timeout in seconds

        Returns:
            bool: True if the element exists, False otherwise
        """
        logger.info(f"Enter IsExist from {name} ...")
        wait = self._wait_for_element(timeout)
        self._waitBeforeAction(500)
        element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
        self._HighlightElement(element)
        logger.info(f"Exit IsExist from {name} ...")
        return True

    # @handle_exceptions_with_retry(retries=1, delay=0)
    def _isElementExisting(self, name, selector, timeout):
        """
        Check if the element exists.
        Args:
            name (str): name of action
            selector (str): selector of the element
            timeout (Timeout): timeout duration
        Returns:
            WebElement or None: Element if found, None otherwise
        """
        print(f"Enter {name} action selector: {selector}")
        if self.found_event.is_set():  # Check if element is already found
            return

        try:
            wait_time = timeout.value  # Total wait time from the Timeout enum
            poll_interval = 0.5  # Check every 0.5 seconds

            for _ in range(int(wait_time / poll_interval)):
                if self.found_event.is_set():  # Exit if element is already found
                    return

                element = WebDriverWait(self.driver, poll_interval).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )

                with self.lock:
                    if self.result_found is None:  # Only set if no element is found yet
                        self.result_found = element  # Store the found element
                        print(f"Exit {name} action selector: {selector} - Found element")
                        self.found_event.set()  # Signal other threads to stop
                return element  # Return after finding the element

        except Exception as e:
            print(f"Error in {name} action selector: {selector}: {e}")
            return None

    def FindParallel(self, selectors):
        """
        Find existing elements in parallel.
        :param selectors: list of element selectors
        :return: the first existing element or None
        """
        logger.info(f"Enter FindParallel ...")
        threads = []
        for selector in selectors:
            t = threading.Thread(target=self._isElementExisting,
                                 args=("parallel search", selector, Timeout.LONG))
            threads.append(t)
            t.start()

        for t in threads:
            if t.is_alive():
                t.join()  # Wait for all threads to finish

        if self.result_found:
            logger.info(f"Element found: {self.result_found.get_attribute('innerText')}")
        else:
            print("No matching element found.")

        return self.result_found  # Return the found element or None

    def OpenUrl(
            self, name, url: str, delay_before=0, delay_after=0
    ):
        """
        Navigate to the specified URL.

        Args:
            name (str): name of action
            url (str): URL to navigate to
            delay_before (int): delay before the navigation in milliseconds
            delay_after (int): delay after the navigation in milliseconds
        Returns:
            bool: True if the navigation was successful, False otherwise
        """
        logger.info(f"Enter OpenUrl from {name} ...")
        self._waitBeforeAction(delay_before)
        self.driver.get(url)
        self._wait_after_action(delay_after)
        logger.info(f"Exit OpenUrl from {name} ...")
        return True

    def ReadElementText(
            self, name, selector, timeout: Timeout = Timeout.MEDIUM, delay_before=0, delay_after=0
    ) -> str:
        """
        Get the text value of element.

        Args:
            name (str): name of action
            selector (str): selector of the element
            timeout (int): timeout in seconds
            delay_before (int): delay before the read in milliseconds
            delay_after (int): delay after the read in milliseconds

        Returns:
            str: text value of the element
        """
        logger.info(f"Enter ReadElementText from {name} ...")
        self._waitBeforeAction(delay_before)
        wait = self._wait_for_element(timeout)
        element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
        self._HighlightElement(element)
        self._wait_after_action(delay_after)

        logger.info(f"Exit ReadElementText from {name} ...")
        # Prioritize `value` attribute, fallback to text properties.
        for attr in ["value", "text", "innerText"]:
            text = element.get_attribute(attr) or getattr(element, attr, None)
            if text:
                return text

        return "Element text could not be read."

    def WriteInputElement(
            self,
            name,
            selector,
            value: str,
            timeout: Timeout = Timeout.MEDIUM,
            delay_before=0,
            delay_after=0,
    ) -> bool:
        """
        Write to the specified input element.

        Args:
            name (str): name of action
            selector (str): selector of the element
            value (str): value to write
            timeout (Timeout): timeout in seconds
            delay_before (int): delay before the write-up milliseconds
            delay_after (int): delay after the write-up milliseconds

        Returns:
            str: text value of the element

        """
        logger.info(f"Enter WriteInputElement from {name} ...")
        self._waitBeforeAction(delay_before)

        wait = self._wait_for_element(timeout)
        element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
        self._HighlightElement(element)
        element.clear()  # Ensure the field is empty before input.
        element.send_keys(value)
        self._wait_after_action(delay_after)
        logger.info(f"Exiting WriteInputElement from {name} ...")
        return True if element.get_attribute("value") else False

    def ReadElements(
            self, name, selector, timeout: Timeout = Timeout.MEDIUM, delay_before=0, delay_after=0
    ):
        """
        Read All elements with the specified selector

        Args:
            name (str): name of action
            selector (str): selector of the element
            timeout (Timeout): timeout in seconds
            delay_before (int): delay before the read in milliseconds
            delay_after (int): delay after the read in milliseconds

        Returns:
            list: list of elements
        """
        print(f"Enter {name} action")
        logger.info(f"Enter {name} action")
        self._waitBeforeAction(delay_before)
        wait = self._wait_for_element(timeout)
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, selector)))
        self._HighlightElement(elements[0])
        self._wait_after_action(delay_after)
        print(f"Exit {name} action")
        logger.info(f"Exit {name} action")
        return elements

    def _HighlightElement(self, element: WebElement):
        """Highlight the element by changing its border color."""
        if not self.DEBUG_MODE:
            return
        old_style = element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].setAttribute('style', 'border: 3px solid red;')", element
        )
        time.sleep(self.HIGHLIGHT_DURATION)
        self.driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1])", element, old_style
        )

    def _waitBeforeAction(self, delay_before):
        """Wait before performing an action."""
        if delay_before > 0:
            time.sleep(delay_before / 1000)

    def _wait_after_action(self, delay_after):
        """Wait after performing an action."""
        if delay_after > 0:
            time.sleep(delay_after / 1000)

    def ReadTable(self, name, selector, next_selector=None, timeout: Timeout = Timeout.MEDIUM,
                  delay_before=0, delay_after=0):
        """
        Read table with the specified selector and return the data as a list of lists.
        Optionally handles pagination if a `next_selector` is provided.
        :param name:
        :param selector:
        :param timeout:
        :param delay_before:
        :param delay_after:
        :param next_selector: Optional selector for the "next" button if table has pagination
        :return: the data as a list of lists
        """
        logger.info(f"Enter ReadTable from {name} ...")
        self._waitBeforeAction(delay_before)
        wait = self._wait_for_element(timeout)
        table_data = []
        previous_page_data = None

        # Load the first row to use as headers (since there's no <thead> tag)
        table_body = wait.until(EC.presence_of_element_located((By.XPATH, selector + "/tbody")))
        table_rows = table_body.find_elements(By.TAG_NAME, "tr")
        # Get headers from the first row of the table (assuming first row is the header)
        header_row = [header.text for header in table_rows[0].find_elements(By.TAG_NAME, "th")]
        table_data.append(header_row)

        while True:
            # Locate table body and rows
            table_body = wait.until(EC.presence_of_element_located((By.XPATH, selector + "/tbody")))
            table_rows = table_body.find_elements(By.TAG_NAME, "tr")

            current_page_data = []
            for row in table_rows[1:]:  # Skip the first row since it is already used as the header
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = []
                for index, cell in enumerate(cells):
                    if index == 0:  # Special handling for the first <td>
                        # Find the first <a> tag and get its href attribute
                        link = cell.find_element(By.TAG_NAME, "a").get_attribute("href")
                        row_data.append(link)  # Add the link to the row data
                    else:
                        row_data.append(cell.text)  # Add the cell's text for other columns

                if row_data:  # Only add rows that have data
                    current_page_data.append(row_data)

            if current_page_data == previous_page_data:
                # logger.info("Duplicate page detected; assuming last page reached.")
                break

            # Extract data from the table
            table_data.extend(current_page_data)
            previous_page_data = current_page_data

            self._HighlightElement(table_body)
            self._wait_after_action(delay_after)

            # If next_selector is provided, attempt to click the "next" button
            # print("current page data", current_page_data)
            if next_selector:
                try:
                    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, next_selector)))
                    next_btn.click()
                    self._wait_after_action(delay_after)
                except (NoSuchElementException, TimeoutException) as e:
                    # logger.info(f"no more tables found")
                    break

        logger.info(f"Exit ReadTable from {name} ...")
        return table_data

    def Handle_Alert(self, name: str, timeout=Timeout.MEDIUM, delay_before=100, delay_after=0):
        """
        Handle an alert.

        Args:
            name (str): name of action
            timeout (Timeout): timeout in seconds
            delay_before (int): delay before the read in milliseconds
            delay_after (int): delay after the read in milliseconds
        """
        logger.info(f"Enter HandleAlert from {name} ...")
        self._waitBeforeAction(delay_before)
        wait = self._wait_for_element(timeout)
        wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.accept()
        self._wait_after_action(delay_after)
        logger.info(f"Exit HandleAlert from {name} ...")
        return text
