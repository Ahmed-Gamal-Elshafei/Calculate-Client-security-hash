import logging
import time
from functools import wraps
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from library.constants import ClickButton, Timeout
from library.action import Action
from reusables import logging_config
from reusables.custom_exception import CustomException

logger = logging.getLogger(__name__)


def handle_exceptions_with_retry(retries=3, delay=1):
    """Decorator to catch exceptions, retry the action, and log errors."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (NoSuchElementException, TimeoutException, ValueError) as e:
                    last_exception = e
                    logger.error(f"{func.__name__} attempt {attempt + 1} failed: {e.__class__.__name__}")
                    time.sleep(delay)

            raise CustomException(f"{func.__name__} failed after {retries} attempts.",
                                  {"exception_type": last_exception.__class__.__name__,
                                   "exception_message": str(last_exception)})

        return wrapper

    return decorator


class AcmeDashBoardNavigateToWorkItem:
    def __init__(self, driver: webdriver):
        # print(f"{self.__class__.__name__} initialized.")
        self.driver = driver
        self.action = Action(driver)

    @handle_exceptions_with_retry(retries=3, delay=1)
    def start(self, second_retry=False):
        """Execute the navigation action."""
        logger.info(f"{self.__class__.__name__} started.")

        name = "Navigate from dashboard to Work item page "
        selector = "//button[normalize-space()='Work Items']"
        check_select = "//h1[@class='page-header']"
        timeout = Timeout.MEDIUM

        if second_retry:
            if not self._pre_condition(name, selector, timeout):
                if self._post_condition(check_select, timeout):
                    return True
                raise NoSuchElementException("Element not found.")

        # Pre-condition, action, and post-condition checks
        if self._pre_condition(name, selector, timeout):
            self._do_action(name, selector, timeout)

        return self._post_condition(check_select, timeout)

    def _pre_condition(self, name: str, selector: str, timeout=Timeout.MEDIUM) -> bool:
        """Check if the element is present."""
        return self.action.IsExist(name, selector, timeout=timeout)

    def _do_action(self, name: str, selector: str, timeout=Timeout.MEDIUM):
        """Perform the action."""
        self.action.Click(name=name, selector=selector, timeout=timeout, click_button=ClickButton.LEFT)

    def _post_condition(self, test_selector, timeout=Timeout.MEDIUM) -> bool:
        """Check if the action succeeded by reading the element value."""
        if self.action.IsExist("Test Navigate", test_selector, timeout=timeout):
            logger.info(f"{self.__class__.__name__} completed successfully.")
            return True
        raise NoSuchElementException("Element not found.")
