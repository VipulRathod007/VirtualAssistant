import time
import webbrowser
from abc import ABC
from enum import Enum
from typing import Any
from collections import defaultdict
from selenium import common, types
from selenium.webdriver import Chrome, ChromeOptions

from GenUtility.GenUtilities import GenUtilities


class Browser(Enum):
    """
    Enum class represents browsers
    """
    CHROME = 'chrome'
    EDGE = 'edge'
    FIREFOX = 'firefox'


class BrowserFactory(ABC):
    """
    Class represents Browser Factory
    """

    __browserInstances = defaultdict()

    @classmethod
    def getInstance(cls, inDriverPath: str, inBrowser: Browser = Browser.CHROME) -> Chrome | None:
        """
        To get the singleton web driver instance
        :param inDriverPath: Driver path
        :param inBrowser: Browser name
        :return: The respective driver instance if found else None
        """
        GenUtilities.isNoneOrEmpty(inDriverPath)
        if inBrowser not in cls.__browserInstances:
            if inBrowser == Browser.CHROME:
                cls.__browserInstances[inBrowser] = Chrome(
                    executable_path=inDriverPath,
                    options=ChromeOptions().add_experimental_option('detach', True)
                )
            elif inBrowser == Browser.EDGE:
                cls.__browserInstances[inBrowser] = None
            elif inBrowser == Browser.FIREFOX:
                cls.__browserInstances[inBrowser] = None
            else:
                return None
        return cls.__browserInstances[inBrowser]

    @classmethod
    def openNewTab(cls, inURL: str, inBrowser: Browser = Browser.CHROME):
        """
        To open the URL in a new tab
        :param inBrowser: Browser name
        :param inURL: URL to open.
        :return: None
        """
        GenUtilities.isNoneOrEmpty(inURL)
        browserInst = GenUtilities.assure(cls.__browserInstances, inBrowser)
        browserInst.execute_script(f"window.open('{inURL}');")
        browserInst.switch_to.window(browserInst.window_handles[-1])

    @classmethod
    def open(cls, inURL: str, inBrowser: Browser = Browser.CHROME):
        """
        To open the URL in the current tab
        :param inBrowser: Browser name
        :param inURL: URL to open.
        :return: None
        """
        GenUtilities.isNoneOrEmpty(inURL)
        browserInst = GenUtilities.assure(cls.__browserInstances, inBrowser)
        browserInst.get(inURL)
        time.sleep(2)
