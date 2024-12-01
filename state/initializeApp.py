from state.StateMachine import State
from reusables.browser_detection import BrowserDetection
from reusables.recorder import start_recording, stop_recording
from reusables.webdriver import WebDriver


class InitializeApp(State):
    """State to initialize the application."""

    def execute(self, context):
        """Perform initialization tasks."""
        try:
            print("Executing InitializeApp State...")

            # Check and start recording if enabled
            is_record = context.variables.get("dict_bool", {}).get("IsRecord", {}).get("value", False)
            self._check_recording(is_record)

            # Detect browser and OS details
            os_name, browser_name, browser_version = BrowserDetection().get_os_browser_version()

            # Initialize WebDriver
            driver = self._get_driver(browser_name)
            context.variables["driver"] = driver

        except Exception as e:
            print(f"Error in InitializeApp.execute: {e}")
            stop_recording()
            context.terminate = True  # Gracefully terminate on error

    def next_state(self, context):
        """Define the next state."""
        from state.login import Login
        return Login()

    @staticmethod
    def _get_driver(browser_name):
        """Get a WebDriver instance for the given browser."""
        try:
            return WebDriver(browser=browser_name, headless=False).get_driver()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize WebDriver: {e}")

    @staticmethod
    def _check_recording(is_record):
        """Start screen recording if enabled."""
        print(f"Screen recording enabled: {is_record}")
        if is_record:
            try:
                start_recording(
                    output_file_prefix="../Records/output",
                    watermark_text="Infinity Chat",
                    font_size=30,
                    text_color=(255, 255, 255, 128),
                    stroke_color=(0, 0, 0, 255),
                    fps=30,
                )
            except Exception as e:
                raise RuntimeError(f"Failed to start recording: {e}")
