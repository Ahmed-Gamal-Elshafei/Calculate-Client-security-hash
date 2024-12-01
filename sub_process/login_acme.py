from automation.login.acme_login_write.Acme_Login_UserName_Write import AcmeLoginUserNameWrite
from automation.login.acme_login_write.Acme_Login_Password_Write import AcmeLoginPasswordWrite
from automation.login.acme_login_navigate.Acme_Login_NavigateTo_DashBoard import AcmeLoginNavigateToDashBoard
from reusables.custom_exception import CustomException


def login_init(driver, user_name: str, password: str) -> bool:
    function_name = "login_sub_process"
    try:

        url = "https://acme-test.uipath.com/login"
        driver.get(url)

        # Writing the username
        username_write = AcmeLoginUserNameWrite(driver)
        username_write.start(user_name)

        # Writing the password
        password_write = AcmeLoginPasswordWrite(driver)
        password_write.start(password)

        # Navigating to dashboard
        login_button_navigator = AcmeLoginNavigateToDashBoard(driver)
        login_button_navigator.start()

        return True
    except (CustomException, Exception) as e:
        print("take screenshot")
        driver.get_screenshot_as_file(f'../Screenshots/{function_name}.png')
        raise  # Re-raise the exception after logging it
