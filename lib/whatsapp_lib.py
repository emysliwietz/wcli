#!/bin/python3

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
    global driver, wait, ac, o, profile
    driver = d
    wait = w
    ac = a
    o = of
    profile = p


def main():
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
    driver.find_element_by_tag_name("body").send_keys(Keys.TAB)


def down():
    global driver
    driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_DOWN)


def enter():
    driver.find_element_by_tag_name("body").send_keys(Keys.RETURN)


def up():
    driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_UP)


def up_far():
    for i in range(100):
        up()


def top():
    for i in range(10):
        up_far()


def bottom():
    for i in range(10):
        down_far()


def down_far():
    for i in range(100):
        down()


def esc():
    driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)


def double_tab():
    tab()
    tab()


def curr():
    o(driver.switch_to.active_element)


def curr_s():
    return driver.switch_to.active_element


def conv():
    conv = driver.find_elements_by_xpath(conv_name)
    name = conv[0].get_attribute("title")
    o(name)
    return name


def conv_s():
    conv = driver.find_elements_by_xpath(conv_name)
    return conv[0].get_attribute("title")


def unstick():
    for i in range(100):
        if not is_chat_s():
            tab()
            time.sleep(0.1)
        else:
            return
    o("Unsticking failed")


def folder_name(c):
    c = c.replace(os.path.sep, "|")
    d = os.path.join(backup_dir, c)
    return d


def folder(c):
    d = folder_name(c)
    if not os.path.isdir(d):
        os.mkdir(d)
    d = os.path.join(d, "media")
    if not os.path.isdir(d):
        os.mkdir(d)


def ifolder():
    folder(conv_s())


def open_details():
    dbo = driver.find_element_by_xpath(details_button_open)
    dbo.click()


def open_media():
    mbo = driver.find_element_by_xpath(media_button_open)
    mbo.click()
    time.sleep(0.2)
    mbo = driver.find_element_by_xpath(media_img_first)
    mbo.click()


def db_click():
    mbo = driver.find_element_by_xpath(media_img_download)
    mbo.click()


def download_media():
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
    mbo = driver.find_element_by_xpath(media_img_left_button)
    mbo.click()
    download_media()
    mbo = driver.find_element_by_xpath(media_img_left_disabled)
    if mbo.get_attribute("aria-disabled") == "true":
        return False
    return True


def download_all_media():
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
    try:
        dbc = driver.find_element_by_xpath(details_button_close)
        dbc.click()
    except:
        pass


def save_screenshot(c):
    today = datetime.now()
    timestamp = today.strftime("%Y-%m-%d %H:%M:%S")
    c_path = "{}.png".format(os.path.join(folder_name(c), timestamp))
    driver.save_screenshot(c_path)


def check_for_group_img():
    try:
        img = driver.find_element_by_xpath(group_image)
        img.click()
    except:
        pass


def img_save(c):
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
    img_save(conv_s())


def step():
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
    o(driver.switch_to.active_element.text.split("\n")[0])


def is_chat_s():
    conv = conv_s()
    conv = "".join(filter(lambda x: x in string.printable, conv)).strip()
    active = driver.switch_to.active_element.text.split("\n")[0]
    active = "".join(filter(lambda x: x in string.printable, active)).strip()
    return conv == active


def is_chat():
    a = is_chat_s()
    o(a)
    return a


def get_desc():
    try:
        driver.find_element_by_xpath("//span[@class='_1qo6g']").click()
    except:
        pass
    try:
        desc = driver.find_element_by_xpath(no_group_desc)
        o(desc.text)
    except:
        try:
            desc = driver.find_element_by_xpath(group_desc)
            o(desc.text)
        except:
            try:
                desc = driver.find_element_by_xpath(user_desc)
                o(desc.get_attribute("title"))
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
    folder(conv_s())
    o(conv_s())
    isave()
    step_before = True
    step_now = step()
    return step_before, step_now


def backup():
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
