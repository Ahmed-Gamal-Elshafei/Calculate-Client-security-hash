import logging
import time
from functools import wraps
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from library.constants import Timeout
from library.action import Action
from reusables.custom_exception import CustomException
from reusables import logging_config

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


class AcmeLoginUserNameWrite:
    def __init__(self, driver: webdriver):
        # logger.info(f"{self.__class__.__name__} initialized.")
        self.driver = driver
        self.action = Action(driver)

    @handle_exceptions_with_retry(retries=3, delay=1)
    def start(self, value) -> bool:
        """Execute the write operation with pre- and post-condition checks."""
        logger.info(f"{self.__class__.__name__} started.")

        name = "Write Username Input Element"
        selector = "// input[ @ id = 'email']"
        timeout = Timeout.MEDIUM

        # Pre-condition check
        if not self._pre_condition(name, selector, timeout):
            raise NoSuchElementException
        # Perform action
        self._do_action(name, selector, value, timeout)

        # Post-condition check
        if self._post_condition(name, selector, value, timeout):
            logger.info(f"{self.__class__.__name__} finished successfully.")
            return True
        logger.info(f"{self.__class__.__name__} finished with errors.")
        return False

    def _pre_condition(self, name: str, selector: str, timeout=Timeout.MEDIUM) -> bool:
        """Check if the element is present."""
        return self.action.IsExist(name, selector, timeout=timeout)

    def _do_action(self, name: str, selector: str, value: str, timeout=Timeout.MEDIUM):
        """Enter the specified value into the element."""
        self.action.WriteInputElement(
            name, selector, timeout=timeout, value=value, delay_before=0, delay_after=0
        )

    def _post_condition(self, name: str, selector: str, value: str, timeout=Timeout.MEDIUM) -> bool:
        """Verify if the written value matches the expected value."""
        new_value = self.action.ReadElementText(
            name, selector, timeout=timeout, delay_before=100, delay_after=100
        )
        if value == new_value:
            return True
        raise ValueError(f"{self.__class__.__name__} verification failed: Expected '{value}', found '{new_value}'")
