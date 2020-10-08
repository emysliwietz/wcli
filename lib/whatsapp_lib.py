#!/bin/python3

"""Interface with whatsapp web."""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import hashlib
import string
from datetime import datetime
import urllib.request
from os import listdir, mkdir, rename, remove
from os.path import isfile, isdir, join, expanduser, sep
import traceback
import csv
from bs4 import BeautifulSoup
import sys
import re

DOWNLOAD_DIR = join(expanduser("~"), "Downloads")
MEDIA_DIR = "media"
BACKUP_DIR = "backups"

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
v = None
curr_view = None


def init(d, w):
    """Initialize variables on library reload."""
    global driver, wait
    driver = d
    wait = w


def main():
    """Start the webdriver."""
    if not isdir(BACKUP_DIR):
        mkdir(BACKUP_DIR)
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


def go_up():
    """Go one chat up and print name."""
    up()
    conv()


def go_down():
    """Go one chat down and print name."""
    down()
    conv()


def up_far():
    """Send up key 100 times."""
    for i in range(100):
        up()


def top():
    """Go to the very top of the chat list."""
    chats = ["", "", ""]
    for _ in range(10):
        up_far()
        chats += [
            conv_s(),
        ]
        if chats[-1] == chats[-2] == chats[-3]:
            return


def bottom():
    """Go to the very bottom of the chat list."""
    chats = ["", "", ""]
    for _ in range(10):
        down_far()
        chats += [
            conv_s(),
        ]
        if chats[-1] == chats[-2] == chats[-3]:
            return


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


def conv_chat_s():
    """Return name of current chat."""
    conv = driver.find_elements_by_xpath(conv_name)
    return conv[0].get_attribute("title")


def conv_chat():
    """Output name of current chat to the screen."""
    name = conv_chat_s()
    o(name)
    return name


def conv_s():
    """
    Return name of current chat.

    ONLY WORKS IN CHAT VIEW!!!
    For more reliablility (although slower execution), use conv_chat_s instead
    """
    html = driver.switch_to.active_element.get_attribute("innerHTML")
    soup = BeautifulSoup(html, features="lxml")
    that_elem = soup.find("span", {"class": "_357i8"})
    if not that_elem:  # This is a group chat
        that_elem = soup.find("div", {"class": "_357i8"})
    if not that_elem:  # This chat is not saved
        that_elem = soup.find("div", {"class": "_3CneP"})
    try:
        return that_elem.find("span")["title"]
    except:
        return conv_chat_s()


def conv():
    """Output name of current chat to the screen."""
    name = conv_s()
    o(name)
    return name


def num_unread():
    """Print number of unread chats."""
    unread = '//span[@class="_31gEB"]/../../../../../div[@class="_3dtfX"]/div/span'
    a = driver.find_elements_by_xpath(unread)
    o(len(a))


def unread():
    """Print names of unread chats."""
    unread = '//span[@class="_31gEB"]/../../../../../div[@class="_3dtfX"]/div/span'
    a = driver.find_elements_by_xpath(unread)
    a += driver.find_elements_by_xpath(unread + "/span")
    for elem in a:
        title = elem.get_attribute("title")
        if title:
            o(title)


def message(n):
    """Print message number n."""
    n = int(n)
    message = '//div[@class="copyable-text"]'
    a = driver.find_elements_by_xpath(message)
    o(a[n].text)


def last_message():
    """Print last message."""
    message(-1)


def is_message_s():
    """Check if active element is a message."""
    c = curr_s()
    classes = c.get_attribute("class")
    return "message-out" in classes or "message-in" in classes


def is_message():
    """Print if active element is a message."""
    o(str(is_message_s()))


def clean_colon(s):
    """Remove the trailing colon."""
    s = s.strip()
    if s.endswith(":"):
        return s[:-1].strip()
    return s


def iter_replace_image(html, replacements):
    """Replace nth occurence of img tag in html string with nth string in list."""
    regex = re.compile("<.*?>")
    new = html
    for r in replacements:
        new = re.sub(regex, str(r), new, 1)
    return new


def emoji_clean_msg(msg):
    if msg:
        replacements = []
        for i in msg.find_all("img"):
            replacements.append(i.get("alt"))
        msg = msg.decode_contents()
        msg = iter_replace_image(msg, replacements)
    return msg


def message_info_s():
    """Return information about message."""
    message = curr_s()
    html = message.get_attribute("innerHTML")
    soup = BeautifulSoup(html, features="lxml")
    forwarded = soup.find("span", {"class": "Vts9M"})
    sender = clean_colon(
        soup.find("div", {"class": "_3sKvP wQZ0F"}).find("span").get("aria-label")
    )
    date = clean_colon(
        soup.find("div", {"class": "_274yw"})
        .find("div", {"class": "copyable-text"})
        .get("data-pre-plain-text")
    )
    text = soup.find(
        "span", {"class": "_3Whw5 selectable-text invisible-space copyable-text"}
    ).find("span")
    text = emoji_clean_msg(text)
    q_from = soup.find("span", {"class": "_3Whw5"})
    q_from = emoji_clean_msg(q_from)
    q_msg = soup.find("span", {"class": "quoted-mention _3Whw5"})
    q_msg = emoji_clean_msg(q_msg)
    msg = {}
    msg["forwarded"] = not forwarded is None
    msg["sender"] = sender
    msg["date"] = date
    msg["text"] = text
    msg["q_from"] = q_from
    msg["q_msg"] = q_msg
    return msg


def message_info():
    """Print information about message."""
    msg = message_info_s()
    o("Forwarded: " + str(msg["forwarded"]))
    o("Sender: " + str(msg["sender"]))
    o("Date: " + str(msg["date"]))
    o("Text: " + str(msg["text"]))
    o("Quoted from: " + str(msg["q_from"]))
    o("Quoted text: " + str(msg["q_msg"]))


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
    c = c.replace(sep, "|")
    d = join(BACKUP_DIR, c)
    return d


def folder(c):
    """Create a folder for chat used for backup."""
    d = folder_name(c)
    if not isdir(d):
        mkdir(d)
    d = join(d, MEDIA_DIR)
    if not isdir(d):
        mkdir(d)


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


def safe_rename(old_file, new_file):
    """
    Rename old_file into new_file.

    WhatApp saves images by date and time. If two images are sent in the same second, they will
    have the same name. This function numbers the file in succession to ensure no
    files are overwritten.
    Additionally, it removes FireFox marking downloads as duplicated with () notation.
    """
    k = new_file.rfind(".")
    if new_file[:k][-1] == ")":
        j = new_file[:k].rfind("(")
        new_file = new_file[:j] + new_file[k:]
    orig_new_file = new_file
    i = 0
    while isfile(new_file):
        i = orig_new_file.rfind(".")
        new_file = orig_new_file[:i] + f" - {i}" + orig_new_file[i:]
        i += 1
        o(new_file)
    rename(old_file, new_file)


def move_download_files(files, pre_hashlist):
    """Move files that have just been downloaded to backup folder of current chat."""
    for f in files:
        if f.startswith("WhatsApp Video") or f.startswith("WhatsApp Image"):
            d = join(folder_name(conv_s()), MEDIA_DIR, f)
            file_name = join(DOWNLOAD_DIR, f)
            sha256_hash = hashlib.sha256()
            file_hash = ""
            with open(file_name, "rb") as f:
                # Read and update hash string value in blocks of 4K
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
                file_hash = sha256_hash.hexdigest()
            if file_hash not in pre_hashlist:
                safe_rename(file_name, d)
                o(f"Downloaded {d}")
            else:
                remove(file_name)
                o(f"File already exists: {d}")


def get_chat_hashes(curr):
    """Get hashes of all files in a media folder."""
    sha256_hash = hashlib.sha256()
    file_hashes = []
    media_dir = join(folder_name(curr), MEDIA_DIR)
    for filename in listdir(media_dir):
        with open(join(media_dir, filename), "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            file_hashes += [
                sha256_hash.hexdigest(),
            ]
    return file_hashes


def download_media(do_move=True):
    """Wait and download a media file."""
    mbo = driver.find_element_by_xpath(media_img_download)
    for i in range(5):
        if len(driver.find_elements_by_xpath("//div[@class='PVMjB']")) == 11:
            # o("Downloading")
            if do_move:
                files_prev = [
                    f for f in listdir(DOWNLOAD_DIR) if isfile(join(DOWNLOAD_DIR, f))
                ]
            time.sleep(1)
            mbo = driver.find_element_by_xpath(media_img_download)
            mbo.click()
            if do_move:
                time.sleep(1)
                files_after = [
                    f for f in listdir(DOWNLOAD_DIR) if isfile(join(DOWNLOAD_DIR, f))
                ]
                file_hashes = get_chat_hashes(conv_s())
                move_download_files(
                    list(set(files_after) - set(files_prev)), file_hashes
                )
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
    open_media()
    files_prev = [f for f in listdir(DOWNLOAD_DIR) if isfile(join(DOWNLOAD_DIR, f))]
    download_media(do_move=False)
    while left_media():
        pass
    time.sleep(1)
    # to make sure all images finish downloading
    # (there is no direct way to check for finished downloads)
    files_after = [f for f in listdir(DOWNLOAD_DIR) if isfile(join(DOWNLOAD_DIR, f))]
    move_download_files(list(set(files_after) - set(files_prev)))
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
    c_path = "{}.png".format(join(folder_name(c), timestamp))
    driver.save_screenshot(c_path)


def isave_screenshot():
    """Save a screenshot of the currently selected chat."""
    save_screenshot(conv_s())


def maximize():
    """Maximizes the browser."""
    driver.maximize_window()


def goto_exact(chat_name):
    """Open the chat view of contact with name without emojis."""
    chat = no_emojis(chat_name)
    top()
    while True:
        a = conv_s()
        if a == chat:
            return
        else:
            down()
            unstick()
            b = conv_s()
            if a == b:
                o("Chat not found")
                return False


def goto(chat_name):
    """Open the chat view of contact that starts with name without emojis."""
    chat = no_emojis(chat_name).lower()
    top()
    while True:
        a = conv_s().lower()
        if a.startswith(chat):
            return
        else:
            down()
            unstick()
            b = conv_s().lower()
            if a == b:
                o("Chat not found")
                return False
    conv()


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
    img_save(conv_chat_s())


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


def no_emojis(s):
    """Return string without all emojis."""
    return "".join(filter(lambda x: x in string.printable, s)).strip()


def is_chat_s():
    """Return if selected element is a chat list item."""
    conv = conv_s()
    conv = no_emojis(conv)
    active = driver.switch_to.active_element.text.split("\n")[0]
    active = no_emojis(active)
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
