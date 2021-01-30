#!/bin/python3

"""Server to handle selenium on WhatsApp Web."""

import time
import urllib.request
import traceback
import csv
import os
import glob
import sys
from lib import whatsapp_lib as l
from importlib import reload
import curses
from inspect import getmembers, isfunction

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options

print("Waiting for browser to open...")

DOWN_DIR = "downloads"
if not os.path.isdir(DOWN_DIR):
    os.mkdir(DOWN_DIR)

driver = None
wait = None
ac = None


def all_functions():
    """Return all functions in whatsapp_lib library."""
    reload(l)
    return [name for (name, f) in getmembers(l) if isfunction(f)]


def exec_command(c):
    """Execute entered library command."""
    try:
        reload(l)
        l.init(driver, wait)
        c = c.strip()
        ret = {"l": l}
        if " " in c:
            command = c.split(" ")[0]
            arguments = ""
            for i in c.split(" ")[1:]:
                arguments += f' "{i}",'
            if arguments[-1] == ",":
                arguments = arguments[:-1]
            exec(f"x = l.{command}({arguments})", ret)
            return ret["x"]
        else:
            exec("x = l." + c + "()", ret)
            return ret["x"]
    except Exception:
        print(traceback.format_exc())
        return "Error"

def make_profile(profile):
    mozilla_dir = os.path.join(os.path.expanduser("~"), ".mozilla", "firefox", "*")
    list_of_files = [x for x in glob.glob(mozilla_dir) if x.endswith(f".{profile}")]
    latest_file = max(list_of_files, key=os.path.getctime)
    profile = None
    profile = webdriver.FirefoxProfile(latest_file)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/png")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "video/mp4")
    profile.set_preference("browser.download.dir", DOWN_DIR)
    return profile

def main(visible, profile):
    """Start and initialize the library, start main loop."""
    global driver, wait, o, v, curr_view
    if visible:
        print("Browser will open shortly")
    else:
        print("Waiting for headless browser to execute")
    options = Options()
    options.headless = not visible
    profile = make_profile(profile)
    print("Test 1")
    driver = webdriver.Firefox(profile, options=options)
    wait = WebDriverWait(driver, 600)
    ac = ActionChains(driver)
    print("Test 2")
    if visible:
        driver.maximize_window()
    print("Test 3")
    l.init(driver, wait)
    print("Test 4")
    l.main()
    print("WhatsApp Web CLI")
