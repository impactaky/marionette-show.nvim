# -*- coding: utf-8 -*-
import neovim
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from subprocess import Popen


@neovim.plugin
class MarionetteShow(object):
    def __init__(self, vim):
        self.vim = vim
        self.driver = None
        self.geckodriver = None

    def __del__(self):
        if self.geckodriver:
            self.geckodriver.terminate()

    def attach_browser(self):
        self.geckodriver = Popen(
            ['geckodriver', '--connect-existing', '--marionette-port', '2828'])
        caps = DesiredCapabilities.FIREFOX
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444',
            desired_capabilities=caps)

    @neovim.function('_marionette_get')
    def get(self, args):
        if not self.driver:
            self.attach_browser()
        self.driver.get(args[0])
