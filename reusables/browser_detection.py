import subprocess
import platform


class BrowserDetection:
    """
    detect installed browsers and return the version
    """

    def __init__(self):
        pass

    def _get_os(self):
        return platform.system().lower()

    def _get_browser_version(self, os_name, browser_name):
        if os_name == "windows":
            return self._get_browser_version_windows(browser_name)
        elif os_name == "darwin":  # macOS
            return self._get_browser_version_macos(browser_name)
        elif os_name == "linux":
            return self._get_browser_version_linux(browser_name)
        else:
            print(f"Unsupported operating system: {os_name}")
            return None

    def _run_command(self, command):
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0 and result.stdout:
            return result.stdout.strip().split()[-1]
        return None

    def _check_browser_in_path(self, browser_name):
        commands = {
            "chrome": "chrome --version",
            "firefox": "firefox --version",
            "edge": "msedge --version",
            "safari": "safari --version",
            "opera": "opera --version"
        }
        return self._run_command(commands.get(browser_name))

    def _get_browser_version_windows(self, browser_name):
        # First, try using the PATH
        version = self._check_browser_in_path(browser_name)
        if version:
            return version

        # Try to find the browser in the registry
        import winreg
        registry_paths = {
            "chrome": r"Software\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
            "firefox": r"Software\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe",
            "edge": r"Software\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe",
            "safari": r"Software\Apple Computer, Inc.\Safari\CurrentVersion\App\Path",
            "opera": r"Software\Microsoft\Windows\CurrentVersion\App Paths\opera.exe"
        }

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_paths[browser_name])
            executable_path = winreg.QueryValue(key, None)
            version = self._run_command(
                f'powershell -Command "(Get-Item -Path \'{executable_path}\').VersionInfo.ProductVersion"')
            return version
        except FileNotFoundError:
            print(f"{browser_name} not found in registry.")
        except Exception as e:
            print(f"Error accessing registry for {browser_name}: {e}")

        print(f"{browser_name} is not installed.")
        return None

    def _get_browser_version_macos(self, browser_name):
        # Check in PATH as before
        return self._check_browser_in_path(browser_name)

    def _get_browser_version_linux(self, browser_name):
        # Check in PATH as before
        return self._check_browser_in_path(browser_name)

    def get_os_browser_version(self):
        """
        detect installed browsers and return the version
        :return: operating system name, browser name, browser version
        """
        os_name = self._get_os()
        browser_list = ["chrome", "firefox", "edge", "safari","opera"]
        for browser in browser_list:
            browser_version = self._get_browser_version(os_name, browser)
            if browser_version:
                print(f"the {browser} version: {browser_version}")
                return os_name, browser, browser_version
        return os_name, None, None
# def get_os():
#     return platform.system()
# def get_browser_version(os_name, browser_name):
#     if os_name == "windows":
#         return get_browser_version_windows(browser_name)
#     elif os_name == "darwin":  # macOS
#         return get_browser_version_macos(browser_name)
#     elif os_name == "linux":
#         return get_browser_version_linux(browser_name)
#     else:
#         print(f"Unsupported operating system: {os_name}")
#         return None
# def get_browser_version_windows(browser_name):
#     commands = {
#         "chrome": 'powershell -Command "(Get-Item -Path \'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\').VersionInfo.ProductVersion"',
#         "firefox": 'powershell -Command "(Get-Item -Path \'C:\\Program Files\\Mozilla Firefox\\firefox.exe\').VersionInfo.ProductVersion"',
#         "edge": 'powershell -Command "(Get-Item -Path \'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe\').VersionInfo.ProductVersion"'
#     }
#     command = commands.get(browser_name)
#     if not command:
#         print(f"{browser_name} is not supported on Windows.")
#         return None
#
#     result = subprocess.run(command, capture_output=True, text=True, shell=True)
#     if result.returncode == 0 and result.stdout:
#         return result.stdout.strip().split()[-1]
#     # print(f"Failed to retrieve version for {browser_name} on Windows.")
#     return None
#
# def get_browser_version_macos(browser_name):
#     commands = {
#         "chrome": '/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version',
#         "firefox": '/Applications/Firefox.app/Contents/MacOS/firefox --version'
#     }
#     command = commands.get(browser_name)
#     if not command:
#         print(f"{browser_name} is not supported on macOS.")
#         return None
#
#     result = subprocess.run(command, capture_output=True, text=True, shell=True)
#     if result.returncode == 0 and result.stdout:
#         return result.stdout.strip().split()[-1]
#     # print(f"Failed to retrieve version for {browser_name} on macOS.")
#     return None
#
# def get_browser_version_linux(browser_name):
#     commands = {
#         "chrome": 'google-chrome --version',
#         "firefox": 'firefox --version'
#     }
#     command = commands.get(browser_name)
#     if not command:
#         print(f"{browser_name} is not supported on Linux.")
#         return None
#
#     result = subprocess.run(command, capture_output=True, text=True, shell=True)
#     if result.returncode == 0 and result.stdout:
#         return result.stdout.strip().split()[-1]
#     # print(f"Failed to retrieve version for {browser_name} on Linux.")
#     return None
#
#
# def get_os_browser_version():
#     os_name = get_os()
#     browser_list = ["chrome", "firefox", "edge"]
#     for browser in browser_list:
#         browser_version = get_browser_version(os_name, browser)
#         if browser_version:
#             print(f"the {browser} version: {browser_version}")
#             return os_name, browser, browser_version
#     return os_name, None, None


# get_os_browser_version()
