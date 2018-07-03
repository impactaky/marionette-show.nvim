# -*- coding: utf-8 -*-
import neovim
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from subprocess import Popen


@neovim.plugin
class MarionetteShow(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.driver = None
        self.geckodriver = None

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
        if is_remote == 1:
            pass
        else:
            exec('self.driver = webdriver.{}({})'.format(driver_type, arg))

    @neovim.function('_marionette_get', sync=True)
    def get(self, args):
        if not self.driver:
            self.attach_browser()
        self.driver.get(args[0])
