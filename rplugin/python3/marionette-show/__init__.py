# -*- coding: utf-8 -*-
import neovim
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
import os

@neovim.plugin
class MarionetteShow(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.driver = None
        self.geckodriver = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def __del__(self):
        if self.geckodriver:
            self.geckodriver.terminate()

    def attach_browser(self):
        is_remote = self.nvim.eval('g:marionette_show#remote#enable')
        driver_type = self.nvim.eval('g:marionette_show#driver_type')
        if driver_type ==0:
            self.nvim.command("echomsg 'Please set g:marionette_show#driver_type'")
            return
        if driver_type == 'Firefox':
            caps = DesiredCapabilities.FIREFOX
            arg  = ''
        elif driver_type == 'Chrome':
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-infobars")
            caps = options.to_capabilities()
            arg  = "chrome_options=options"

        resume_enabled = self.nvim.eval('g:marionette_show#resume#enable')

        if is_remote == 1:
            url = self.nvim.eval('g:marionette_show#remote#url')
            self.driver = webdriver.Remote(command_executor=url, desired_capabilities=caps)
        else:
            exec('self.driver = webdriver.{}({})'.format(driver_type, arg))
        if resume_enabled :
            with open("{}/session_id.txt".format(self.current_dir), "w") as f:
                f.write(self.driver.session_id)


    def current_url(self):
        if not self.driver:
            return None
        try:
            ret = self.driver.current_url
            return ret
        except WebDriverException:
            return None

    @neovim.function('_marionette_get', sync=False)
    def get(self, args):
        if not self.current_url() :
            self.attach_browser()
        self.driver.get(args[0])

