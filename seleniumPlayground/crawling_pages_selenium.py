#!/usr/bin/env python

from pyvirtualdisplay import Display
from selenium import webdriver
import os
import re


'''gets links of items on Sale and returns it'''


def get_link_list(home, item_link_list):
    print(home.current_url)
    item_list = home.find_elements_by_xpath('//article[@class="panel product sector-electronics "]/a[1]')
    print(len(item_list))

    for item in item_list:
        item_link_list.append(item.get_attribute('href'))
    return


'''loads the whol page and returns the links to items on it'''


def extract_item_count(home):
    item_count_str = home.find_element_by_xpath('//div[@class="col-xs-12 col-sm-4"]')

    item_count_str = re.findall(r'\d+', item_count_str.text)
    maxpower = len(item_count_str) - 1
    item_count = 0
    for i in range(maxpower + 1):
        item_count += pow(10, maxpower * 3) * int(item_count_str[i])
        maxpower -= 1
    print("extracted item count")
    return item_count


def get_item_list(home, base_adress):
    item_count = extract_item_count(home)
    home.get(base_adress + str(item_count))
    item_link_list = []
    prev_ic = -1
    while len(item_link_list) > prev_ic:
        prev_ic = len(item_link_list)
        home.get(base_adress + "skip=" + str(len(item_link_list)) + "&take=" + str(item_count))
        get_link_list(home, item_link_list)
        print("got" + str(len(item_link_list)) + " items")

    return item_link_list


'''crawls the whole digitec page for sales items and saves there links in a file called "link_file.txt"'''


def crawl_page():
    # Opening virtual display to run program in background
    display = Display(visible=0, size=(800, 600))
    display.start()

    # Starts the browser and opens the first page
    home = webdriver.Chrome()
    home.get("https://www.digitec.ch/de/Sale")

    print("started the crawling function")
    item_list = get_item_list(home, "https://www.digitec.ch/de/Sale?")

    # removes the file "link_file.txt" and handles if not existent
    try:
        os.remove("link_file.txt")
    except FileNotFoundError:
        print("FileNotFound:    link_file.txt does not exist")

    link_file = open("link_file.txt", 'w')

    for item in item_list:
        link_file.write(item + "\n")

    home.close()

    # Closes the display again
    display.stop()


crawl_page()
