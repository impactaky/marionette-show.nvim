# -*- coding: utf-8 -*-
import neovim
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from MarionetteShow.attach import attach_browser


@neovim.plugin
class MarionetteShow(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.driver = None

    def check_driver(self):
        if not self.driver:
            self.driver = attach_browser(self.nvim)
            if self.driver == None:
                nvim.command("echomsg 'Can't attach browser'")
                exit()
            return
        try:
            ret = self.driver.current_url
            return ret
        except WebDriverException:
            self.driver = attach_browser(self.nvim)
            if self.driver == None:
                nvim.command("echomsg 'Can't attach browser'")
                exit()
            return

    @neovim.function('_marionette_get', sync=False)
    def get(self, args):
        self.check_driver()
        self.driver.get(args[0])
