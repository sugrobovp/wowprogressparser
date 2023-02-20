from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

cached_count = {}

def game(step, page_num):
    count = 0
    search = True
    while search:
        url = f'https://classic.warcraftlogs.com/zone/rankings/1017#metric=progress&boss=744&page={page_num}'
        driver = webdriver.Chrome('~\Downloads\chromedriver_linux64\chromedriver')

        driver.get(url)
        xpath = f'//*[@id="row-744-{(page_num - 1) * 50 + 1}"]/td[9]'
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
        res = driver.page_source

        bs = BeautifulSoup(res, 'lxml')
        a = bs.find_all("td", class_='main-table-number hm-cell')
        row = 1
        for el in a:
            if el.text == '4 Towers':
                count += 1
                row += 1
            else:
                cached_count[page_num] = count
                if step == 10:
                    game(step=1, page_num=page_num-10)
                if step == 1:
                    cached_count.update({'page': page_num, 'row': row - 1})
                    return
                search = False
                break
        page_num += step
    res = (cached_count['page'] - 1) * 50 + cached_count['row']
    return res


print(game(step=10, page_num=1))



