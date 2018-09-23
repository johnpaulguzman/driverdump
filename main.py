#!/usr/bin/env python3
# Usage: python main.py <USERNAME> <PASSWORD>

import os
import sys
import time

import selenium.webdriver


fobj = lambda o, s: [v for v in dir(o) if s in v]
clear = lambda: print('\x1bc', end="\n" * 50)
beep = lambda: print('\a')

checks = [lambda s: "am" in s.lower(), lambda s: "5th" in s.lower()]
(_, username, password, *_) = sys.argv
(username_element, password_element, login_element) = ("m_login_email", "m_login_password", "u_0_5")
(story_element) = ("story_body_container")
chrome_driver = os.path.join(os.getcwd(), "chromedriver.exe")
chrome_arguments = ["--headless", "--window-size=1920x1080"]

chrome_options = selenium.webdriver.chrome.options.Options()
for arg in chrome_arguments: chrome_options.add_argument(arg)
story_store = set()

with selenium.webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver) as driver:
    driver.get("https://m.facebook.com/") ; time.sleep(6)
    username_field = driver.find_element_by_id(username_element)
    username_field.send_keys(username) ; time.sleep(6)
    password_field = driver.find_element_by_id(password_element)
    password_field.send_keys(password) ; time.sleep(6)
    login_button = driver.find_element_by_id(login_element)
    login_button.click() ; time.sleep(6)
    while True:
        clear()
        print("Querying group...")
        driver.get("https://m.facebook.com/groups/blscarpool/") ; time.sleep(6)
        stories = driver.find_elements_by_class_name(story_element) ; time.sleep(6)
        old_len = len(story_store)
        for story in stories:
            story_text = story.text.encode('ascii', 'ignore').decode('ascii', 'ignore')
            if all(check(story_text) for check in checks):
                story_store.add(story_text)
        for story_text in story_store:
            print(story_text, end="\n========\n")
        print(f"Number of stories: {len(story_store)}")
        if old_len != len(story_store): beep() ; time.sleep(6) ; beep() ; time.sleep(6) ; beep()
        time.sleep(6)
print("Done!")

""" NOTES
pipenv --tree
pipenv shell

def tracefunc(frame, event, arg, indent=[0]):
      if event == "call":
          indent[0] += 2
          print "-" * indent[0] + "> call function", frame.f_code.co_name
      elif event == "return":
          print "<" + "-" * indent[0], "exit function", frame.f_code.co_name
          indent[0] -= 2
      return tracefunc

import sys
sys.settrace(tracefunc)
"""