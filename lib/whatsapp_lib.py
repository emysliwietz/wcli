#!/bin/python3

"""Interface with whatsapp web."""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import string
from datetime import datetime
import urllib.request
import traceback
import csv
import os
import sys

LAST_MESSAGES = 4
WAIT_FOR_CHAT_TO_LOAD = 2  # in secs

backup_dir = "backups"

message_dic = {}
chat_dict = {}

notifications = '//div[@class="_2kJqr"]'
chat_class = '//div[@class="_210SC"]'
group_name = '//div[@class="_357i8"]'
chat_name = '//div[@class="_3CneP"]'
conv_name = '//div[@class="DP7CM"]//span'
details_button_open = '//header[@class="_1iFv8"]'
details_button_close = '//button[@class="t4a8o"]'
media_button_open = '//div[@class="sb_Co"]'
media_img_first = '//div[@class="_2n28r"]'
media_img_download = (
    "/html/body/div[1]/div/span[3]/div/div/div[2]/div[1]/div[2]/div/div[4]"
)
media_img_left_button = (
    "/html/body/div[1]/div/span[3]/div/div/div[2]/div[2]/div[1]/div/span"
)
media_img_left_disabled = (
    "/html/body/div[1]/div/span[3]/div/div/div[2]/div[2]/div[1]/div"
)
image = '//div[@class="IR_0S"]//div//img'
image2 = '//div[@class="H36t4"]//div//img'
group_image = "/html/body/div[1]/div/span[4]/div/ul/li[1]/div"
big_image = '//div[@class="_2bPiN"]//img'
no_group_desc = '//div[@class="TX5f-"]'
group_desc = '//div[@class="_3sKYI"]//span'
user_desc = '//span[@class="_1X4JR"]//span'


first = None

driver = None
wait = None
ac = None
o = None
profile = None


def init(d, w, a, of, p):
    """Initialize variables on library reload."""
    global driver, wait, ac, o, profile
    driver = d
    wait = w
    ac = a
    o = of
    profile = p


def main():
    """Start the webdriver."""
    if not os.path.isdir(backup_dir):
        os.mkdir(backup_dir)
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 600)
    # print("Waiting for notification thingy to appear")
    # nots = wait.until(EC.presence_of_element_located((By.XPATH, notifications)))
    wait.until(EC.presence_of_element_located((By.XPATH, chat_class)))
    try:
        double_tab()
        tab()
    except:
        pass


def tab():
    """Send a tab key."""
    driver.find_element_by_tag_name("body").send_keys(Keys.TAB)


def down():
    """Send an arrow down key."""
    global driver
    driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_DOWN)


def enter():
    """Send an enter key."""
    driver.find_element_by_tag_name("body").send_keys(Keys.RETURN)


def up():
    """Send an arrow up key."""
    driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_UP)


def up_far():
    """Send up key 100 times."""
    for i in range(100):
        up()


def top():
    """Go to the very top of the chat list."""
    for i in range(10):
        up_far()


def bottom():
    """Go to the very bottom of the chat list."""
    for i in range(10):
        down_far()


def down_far():
    """Send down key 100 times."""
    for i in range(100):
        down()


def esc():
    """Send escape key."""
    driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)


def double_tab():
    """Send tab key twice."""
    tab()
    tab()


def curr():
    """Output active element to the screen."""
    o(driver.switch_to.active_element)


def curr_s():
    """Return name of active element."""
    return driver.switch_to.active_element


def conv_s():
    """Return name of current chat."""
    conv = driver.find_elements_by_xpath(conv_name)
    return conv[0].get_attribute("title")


def conv():
    """Output name of current chat to the screen."""
    name = conv_s()
    o(name)
    return name


def unstick():
    """Make sure focus is on chat list."""
    for i in range(100):
        if not is_chat_s():
            tab()
            time.sleep(0.1)
        else:
            return
    o("Unsticking failed")


def folder_name(c):
    """Return salitized name of chat to be used as a folder name."""
    c = c.replace(os.path.sep, "|")
    d = os.path.join(backup_dir, c)
    return d


def folder(c):
    """Create a folder for chat used for backup."""
    d = folder_name(c)
    if not os.path.isdir(d):
        os.mkdir(d)
    d = os.path.join(d, "media")
    if not os.path.isdir(d):
        os.mkdir(d)


def ifolder():
    """Create a folder for current chat used for backup."""
    folder(conv_s())


def open_details():
    """Open the details page of a chat."""
    dbo = driver.find_element_by_xpath(details_button_open)
    dbo.click()


def open_media():
    """
    Open the media page of a chat.

    Must be activated on details page
    """
    mbo = driver.find_element_by_xpath(media_button_open)
    mbo.click()
    time.sleep(0.2)
    mbo = driver.find_element_by_xpath(media_img_first)
    mbo.click()


def db_click():
    """Click the download button in media page."""
    mbo = driver.find_element_by_xpath(media_img_download)
    mbo.click()


def download_media():
    """Wait and download a media file."""
    mbo = driver.find_element_by_xpath(media_img_download)
    for i in range(5):
        if len(driver.find_elements_by_xpath("//div[@class='PVMjB']")) == 11:
            o("Downloading")
            time.sleep(1)
            mbo = driver.find_element_by_xpath(media_img_download)
            mbo.click()
            return
        else:
            time.sleep(2)
    o("Downloading failed")


def left_media():
    """Go left in media screen. Return false if at the end."""
    mbo = driver.find_element_by_xpath(media_img_left_button)
    mbo.click()
    download_media()
    mbo = driver.find_element_by_xpath(media_img_left_disabled)
    if mbo.get_attribute("aria-disabled") == "true":
        return False
    return True


def download_all_media():
    """Download all media files of a chat, must be activated in chat view."""
    # download_path = '{}'.format(os.path.join(folder_name(conv_s()), "media"))
    # profile.set_preference("browser.download.dir", download_path)
    open_media()
    download_media()
    while left_media():
        pass
    esc()
    esc()
    o("Finished downloading media")


def close_details():
    """Close details page."""
    try:
        dbc = driver.find_element_by_xpath(details_button_close)
        dbc.click()
    except:
        pass


def save_screenshot(c):
    """Save a screenshot of the current view."""
    today = datetime.now()
    timestamp = today.strftime("%Y-%m-%d %H:%M:%S")
    c_path = "{}.png".format(os.path.join(folder_name(c), timestamp))
    driver.save_screenshot(c_path)


def check_for_group_img():
    """Check if the group has a profile picture."""
    try:
        img = driver.find_element_by_xpath(group_image)
        img.click()
    except:
        pass


def img_save(c):
    """Save the profile picture of chat."""
    open_details()
    time.sleep(1)
    try:
        img = driver.find_element_by_xpath(image)
        img.click()
        check_for_group_img()
    except:
        try:
            img = driver.find_element_by_xpath(image2)
            img.click()
            check_for_group_img()
        except:
            esc()
            time.sleep(1)
            save_screenshot(c)
            close_details()
            o("No profile picture or saving failed")
            return
    # big_img = driver.find_element_by_xpath(big_image)
    # big_url = big_img.get_attribute("src")
    time.sleep(2)
    save_screenshot(c)
    #    js = """
    #    var a = document.createElement('a');
    #    a.href = '{}';
    #    a.download = 'output.png';
    #    document.body.appendChild(a);
    #    a.click();
    #    document.body.removeChild(a);
    #    """.format(big_img.get_attribute("src"))
    #    driver.execute_async_script(js)
    esc()
    time.sleep(1)
    close_details()


def isave():
    """Save profile picture of current chat."""
    img_save(conv_s())


def step():
    """Backup single chat, return False if at the end."""
    c = conv_s()
    down()
    time.sleep(1)
    d = conv_s()
    if c == d:
        unstick()
        return False
    o(d)
    folder(c)
    isave()
    return True


def active():
    """Print currently active element to screen."""
    o(driver.switch_to.active_element.text.split("\n")[0])


def is_chat_s():
    """Return if selected element is a chat list item."""
    conv = conv_s()
    conv = "".join(filter(lambda x: x in string.printable, conv)).strip()
    active = driver.switch_to.active_element.text.split("\n")[0]
    active = "".join(filter(lambda x: x in string.printable, active)).strip()
    return conv == active


def is_chat():
    """Print if selected element is a chat list item to the screen."""
    a = is_chat_s()
    o(a)
    return a


def get_desc():
    """Return and print description of current chat to the screen in details view."""
    try:
        driver.find_element_by_xpath("//span[@class='_1qo6g']").click()
    except:
        pass
    try:
        desc = driver.find_element_by_xpath(no_group_desc)
        o(desc.text)
        return desc.text
    except:
        try:
            desc = driver.find_element_by_xpath(group_desc)
            o(desc.text)
            return desc.text
        except:
            try:
                desc = driver.find_element_by_xpath(user_desc)
                o(desc.get_attribute("title"))
                return desc.text
            except:
                o("Getting description failed")


# def save_images(end):
#    # still gets stuck
#    while(conv() != end):
#        isave()
#        time.sleep(0.5)
#        down()
#        time.sleep(0.5)


def backup_pre():
    """Pre-routine for backing up chats."""
    folder(conv_s())
    o(conv_s())
    isave()
    step_before = True
    step_now = step()
    return step_before, step_now


def backup():
    """Backup all chats."""
    step_before, step_now = backup_pre()
    while step_before or step_now:
        step_before = step_now
        step_now = step()
    folder(conv())
    isave()
    for i in range(4):
        tab()
    c = conv_s()
    o("Done with listing, ended at " + c)
    top()
