import logging
import time
from functools import wraps
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException
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
                except (NoSuchElementException, TimeoutException, ValueError, NoAlertPresentException) as e:
                    last_exception = e
                    logger.error(f"{func.__name__} attempt {attempt + 1} failed: {e.__class__.__name__}")
                    time.sleep(delay)

            raise CustomException(f"{func.__name__} failed after {retries} attempts.",
                                  {"exception_type": last_exception.__class__.__name__,
                                   "exception_message": str(last_exception)})

        return wrapper

    return decorator


class WorkItemUpdatePageConfirmForm:
    def __init__(self, driver: webdriver):
        # print(f"{self.__class__.__name__} initialized.")
        self.driver = driver
        self.action = Action(driver)

    @handle_exceptions_with_retry(retries=3, delay=1)
    def start(self):
        """Execute the navigation action."""
        logger.info(f"{self.__class__.__name__} started.")

        name = "Confirm work item update"
        selector = "//button[@id='buttonUpdate']"
        timeout = Timeout.MEDIUM

        # Pre-condition, action, and post-condition checks
        if not self._pre_condition(name, selector, timeout):
            raise NoSuchElementException
        self._do_action(name, selector, timeout)

        return self._post_condition(name, timeout)

    def _pre_condition(self, name: str, selector: str, timeout=Timeout.MEDIUM) -> bool:
        """Check if the element is present."""
        return self.action.IsExist(name, selector, timeout=timeout)

    def _do_action(self, name: str, selector: str, timeout=Timeout.MEDIUM):
        """Perform the action."""
        self.action.Click(name=name, selector=selector, timeout=timeout, click_button=ClickButton.LEFT)

    def _post_condition(self, name, timeout=Timeout.MEDIUM) -> bool:
        """Check if the action succeeded by reading the element value."""
        alert_text: str = self.action.Handle_Alert(name, timeout=timeout)
        if "Work Item was updated accordingly" in alert_text:
            logger.info(f"{self.__class__.__name__} completed successfully.")
            return True
        raise ValueError("Failed to update work item.")
