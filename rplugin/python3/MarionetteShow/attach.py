import neovim
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
import os


def attach_browser(nvim):

    is_remote = nvim.eval('g:marionette_show#remote#enable')
    driver_type = nvim.eval('g:marionette_show#driver_type')
    resume_enabled = nvim.eval('g:marionette_show#remote#resume#enable')

    if driver_type == 'Firefox':
        exec_driver = webdriver.Firefox
        caps = DesiredCapabilities.FIREFOX
        arg = {}
    elif driver_type == 'Chrome':
        exec_driver = webdriver.Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        caps = options.to_capabilities()
        arg = {'chrome_options': options}
    else:
        nvim.command(
            "echomsg 'g:marionette_show#driver_type is invalid value'")
        return

    if is_remote == 1:
        url = nvim.eval('g:marionette_show#remote#url')
        if resume_enabled:
            return resume_session(
                command_executor=url, desired_capabilities=caps)
        else:
            return webdriver.Remote(
                command_executor=url, desired_capabilities=caps)
    else:
        return exec_driver(**arg)


def resume_session(command_executor, desired_capabilities):

    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        with open("{}/session_id.txt".format(plugin_dir), "r") as f:
            session_id = f.readline()
    except IOError:
        return webdriver.Remote(
            command_executor=command_executor,
            desired_capabilities=desired_capabilities)

    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
    execute = RemoteWebDriver.execute

    def resume_execute(self, command, params=None):
        if command == "newSession":
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return execute(self, command, params)

    RemoteWebDriver.execute = resume_execute

    driver = webdriver.Remote(
        command_executor=command_executor, desired_capabilities={})
    original_session_id = driver.session_id
    RemoteWebDriver.execute = execute

    try:
        driver.current_url
        return driver
    except WebDriverException:
        driver = webdriver.Remote(
            command_executor=command_executor,
            desired_capabilities=desired_capabilities)
        with open("{}/session_id.txt".format(plugin_dir), "w") as f:
            f.write(driver.session_id)
        return driver
