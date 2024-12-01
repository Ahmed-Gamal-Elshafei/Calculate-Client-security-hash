from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class WebDriver:
    def __init__(self, browser="chrome", headless=False, driver_path=None, remote_url=None):
        """
        Initialize the WebDriver with the specified browser type.
        :param browser: "chrome", "firefox", or "edge"
        :param headless: Run browser in headless mode if True
        :param driver_path: Path to the WebDriver executable (optional if in PATH)
        :param remote_url: URL of the remote Selenium server (if using RemoteWebDriver)
        """
        self.browser = browser.lower()
        self.headless = headless
        self.driver_path = driver_path
        self.remote_url = remote_url
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        """
        Set up browser options and capabilities
        :return: driver of specified browser
        """
        # Set up browser options and capabilities
        if self.browser == "chrome":

            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless")

            if self.remote_url:
                return webdriver.Remote(command_executor=self.remote_url,  options=options)
            else:
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)

        elif self.browser == "firefox":
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")

            if self.remote_url:
                return webdriver.Remote(command_executor=self.remote_url,  options=options)
            else:
                service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=options)

        elif self.browser == "edge":
            options = EdgeOptions()
            if self.headless:
                options.add_argument("--headless")

            if self.remote_url:
                return webdriver.Remote(command_executor=self.remote_url, options=options)
            else:
                service = EdgeService(EdgeChromiumDriverManager().install())
                return webdriver.Edge(service=service, options=options)

        else:
            raise ValueError("Unsupported browser. Choose from 'chrome', 'firefox', or 'edge'.")

    def get_driver(self) -> webdriver:
        """
        Return the initialized WebDriver instance.
        """
        return self.driver

    def quit(self):
        """
        Quit the WebDriver instance.
        """
        if self.driver:
            self.driver.quit()

