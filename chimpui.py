from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sched
import time
import io
import zipfile
import os
import requests
import re


DELAY = None
DIRECTORY = None


def init_config():
    with open("chimp.cfg", encoding="utf-8") as file:
        global DELAY
        global DIRECTORY

        string = file.read()
        delaypattern = re.compile(r"(?<=Delay=).*")
        dirpattern = re.compile(r"(?<=WoWDirectory=).*")
        found = delaypattern.search(string)
        DELAY = int(found.group()) if found else 60
        found = dirpattern.search(string)
        DIRECTORY = found.group() if found else ""


def schedule_event(delay):
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(delay, 1, update_elvui)

    scheduler.run()


def update_elvui():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    try:
        driver.get("https://www.tukui.org/download.php?ui=elvui")
        assert "Tukui" in driver.title, "PROP"

        elem = driver.find_element_by_class_name(
            "btn-large")

        link = elem.get_attribute("href")

        driver.close()

        pattern = re.compile(r"\d+(.)+\d[^.zip]")
        version = pattern.search(link)

        print("ElvUI version %s" % (version.group()))
        print("Downloading Elvui from %s." % (link))

        res = requests.get(link)

        print("Extracting Files to current Directory.")
        downzip = zipfile.ZipFile(io.BytesIO(res.content))

        downzip.extractall(path=DIRECTORY)

        downzip.close()
        print("Done...Process will repeat in %d seconds." % (DELAY))
        schedule_event(DELAY)
    except (KeyboardInterrupt, SystemExit):
        print("Process stopped, goodbye......")
    except:
        pass


init_config()
update_elvui()
