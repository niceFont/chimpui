from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import io
import zipfile
import os
import requests
import re


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(chrome_options=chrome_options)

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

downzip.extractall()

downzip.close()

print("Done :  )")
