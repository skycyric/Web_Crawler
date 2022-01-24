import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.youtube.com/c/%E5%81%A5%E5%BA%B720health20/videos")


def collectLinks():
    elements = []
    elems = driver.find_elements_by_xpath("//a[@href]")
    print("Collecting links...")
    for elem in elems:
        elements.append(str(elem.get_attribute("href")))

    for i in elements:
        print(i)


collectLinks()
driver.quit()
