import logging
import time
from functools import wraps
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from library.constants import Timeout
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


class WorkItemClientDataRead:
    def __init__(self, driver: webdriver):
        logger.info(f"{self.__class__.__name__} initialized.")
        self.driver = driver
        self.action = Action(driver)

    @handle_exceptions_with_retry(retries=3, delay=1)
    def start(self) -> str | None:
        """Execute the read operation with pre- and post-condition checks."""
        logger.info(f"{self.__class__.__name__} started.")

        name = "Read client id from work item page"
        selector = "/html/body/div/div[2]/div/div[2]/div/div/div[1]/p"
        timeout = Timeout.MEDIUM
        # Pre-condition check
        if not self._pre_condition(name, selector, timeout):
            raise NoSuchElementException
            # Perform action and check post-condition
        value = self._do_action(name, selector, timeout)
        if self._post_condition(value):
            logger.info(f"{self.__class__.__name__} finished successfully.")
            return value

        logger.info(f"{self.__class__.__name__} finished with errors.")
        return None

    def _pre_condition(self, name: str, selector: str, timeout=Timeout.MEDIUM) -> bool:
        """Check if the element is present."""
        return self.action.IsExist(name, selector, timeout=timeout)

    def _do_action(self, name: str, selector: str, timeout=Timeout.MEDIUM) -> str:
        """Read the text from the element."""
        return self.action.ReadElementText(
            name, selector, timeout=timeout, delay_before=100, delay_after=100
        )

    def _post_condition(self, value: str) -> bool:
        """Verify the action by checking the read value."""
        if value:
            return True
        raise ValueError(f"{self.__class__.__name__} failed: Empty or None value.")
