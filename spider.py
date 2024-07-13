import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
import time
import re

# Edge in headless mode
edge_options = EdgeOptions()
edge_options.use_chromium = True
driver = Edge(executable_path="C:/Users/Blueee/Desktop/database_course/msedgedriver.exe")

# 開啟登入網頁
login_url = "https://www.cosdna.com/cht/user/login.php"
driver.get(login_url)

####################################登入######################################
# 輸入帳號和密碼並登入
driver.find_element(By.NAME,"account").send_keys("tingannlin9085@gmail.com")
driver.find_element(By.NAME,"password").send_keys("***lin****")
driver.find_element(By.CSS_SELECTOR,".btn-primary").click()
############################################################################

# 找到輸入框，輸入品牌名並按下搜尋
driver.find_element(By.NAME,"q").send_keys("1028")
driver.find_element(By.CSS_SELECTOR,".btn-gray.w-full.mt-6").click()
time.sleep(0.2)

# 找到每一個商品
table = driver.find_element(By.CSS_SELECTOR, ".w-full.max-w-full")
prod_rows = table.find_elements(By.CSS_SELECTOR, "tr.hover\\:bg-gray-100")
link_list = []

# 一個一個抓取每個產品的連結
for prod_row in prod_rows:                                                     
    link_element = prod_row.find_element(By.CSS_SELECTOR, "a.inline-block.w-full")
    link_list.append(link_element.get_attribute("href"))

print(link_list)

# 增加搜尋頁數
page_number_list = [2, 3, 4, 5, 6, 7, 8, 9]
for i in page_number_list:
    driver.get(f"https://www.cosdna.com/cht/product.php?q=1028&p={i}")
    table = driver.find_element(By.CSS_SELECTOR, ".w-full.max-w-full")
    rows = table.find_elements(By.CSS_SELECTOR, "tr.hover\\:bg-gray-100")
    for row in rows:
        link_element = row.find_element(By.CSS_SELECTOR, "a.inline-block.w-full")
        link_list.append(link_element.get_attribute("href"))

print(link_list)

# 到每一個商品頁抓詳細資料
data = []
for product_link in link_list:
    driver.get(f"https://www.cosdna.com/cht/{product_link}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    product_dict = dict()
    brand_name = soup.select(".brand-name")
    if len(brand_name) > 0 and len(brand_name[0].contents) > 0:
        product_dict["brand"] = brand_name[0].contents[0]
        product_name = soup.select(".prod-name")
        if len(product_name) > 0:
            product_dict["produce"] = product_name[0].contents[0]
            elements = soup.select(".colors")
            elements_list = []
            for ele in elements:
                item = ele.contents[0]
                elements_list.append(item)
            product_dict["elements"] = elements_list
            data.append(product_dict)  
print(data)

driver.close()
