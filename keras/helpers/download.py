#%%
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
import shutil
from urllib.parse import urlparse
import os

# %%
url = "https://www.google.com/search?q=geometric%20pattern&tbm=isch&hl=en-US&tbs=isz:i&sa=X&ved=0CAEQpwVqFwoTCICX_L3Cvf0CFQAAAAAdAAAAABAC&biw=1448&bih=1059"
# response = requests.get(url)
# html = response.content


#%%
browser = webdriver.Firefox()
browser.get(url)

time.sleep(0.5)

# for button in WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//button[text()='Reject all']"))):
#   button.click()
buttons = browser.find_elements_by_xpath("//button[text()='Reject all']")
for button in buttons:
    button.click()

for i in range(10):
    time.sleep(0.5)
    print("Scrolling ...")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
html = browser.page_source
browser.close()

# %%
parsed = BeautifulSoup(html, 'html.parser')
images = parsed.find_all('img')
links = [img['src'] for img in images if img.has_attr('src') and img['src'].startswith("https")]

# %%
for link in links:
    print(f"downloading image: {link}")
    response = requests.get(link, stream=True)
    parsed = urlparse(link)
    fileName = os.path.basename(parsed.path)
    with open(f"./downloads/{fileName}", "wb") as f:
        shutil.copyfileobj(response.raw, f)
# %%
