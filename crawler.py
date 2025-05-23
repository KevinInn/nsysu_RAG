from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
import os

print("=========爬蟲開始=========")

academic_affairs_pdf_urls = []
student_affairs_pdf_urls = []
placeholder = "https://regs.nsysu.edu.tw/rule/"
sourece_urls = [
    ("https://regs.nsysu.edu.tw/rule/dep_lis?dep=20190816110743016&p=g", academic_affairs_pdf_urls),
    ("https://regs.nsysu.edu.tw/rule/dep_lis?dep=20190816143230017&p=g", student_affairs_pdf_urls),  
]

for source_url, res_list in sourece_urls:
    driver = webdriver.Chrome()
    # url = 'https://regs.nsysu.edu.tw/rule/index'
    driver.get(source_url)

    time.sleep(2)

    ### 定位到"教務處link"，並點擊
    # /html/body/main/div/div/div[1]/ul[1]/li[5]/a
    # /html/body/main/div/div/div[1]/ul[1]/li[6]/a
    # OfficeofAcademicAffairs = WebDriverWait(driver, 5).until(
    #     EC.presence_of_element_located(
    #         (By.XPATH, '/html/body/main/div/div/div[1]/ul[1]/li[6]/a'))
    # )
    # driver.execute_script("arguments[0].click();", OfficeofAcademicAffairs)

    source = driver.page_source  # 刷新html代碼
    soup = BeautifulSoup(source, 'lxml')
    htmls = soup.find_all('table', id='example1')

    for html in htmls:
        # print(f"html: {html}")

        tds = html.find_all('td')  # 找到所有 <td> 標籤

        # print(f"tds: {tds}")

        for i in range(1, len(tds), 4):
            res_list.append(placeholder + tds[i].find('a').attrs.get('href'))

    driver.quit()

print(f"教務處 pdf url:\n{academic_affairs_pdf_urls}")
print(f"學務處 pdf url:\n{student_affairs_pdf_urls}")

print("=========爬蟲結束=========")

# 去教務處的url下載pdf
for i in range(len(academic_affairs_pdf_urls)):

    out_dir = 'data/academic_affairs'
    os.makedirs(out_dir, exist_ok=True)  # 如果資料夾不存在就建立（含多層路徑）

    resp = requests.get(academic_affairs_pdf_urls[i])
    resp.raise_for_status()  # 若失敗會拋出例外

    with open(f'{out_dir}/academic_affairs_{i+1}.pdf', 'wb') as f:
        f.write(resp.content)

# 去學務處的url下載pdf
for i in range(len(student_affairs_pdf_urls)):

    out_dir = 'data/student_affairs'
    os.makedirs(out_dir, exist_ok=True)  # 如果資料夾不存在就建立（含多層路徑）

    resp = requests.get(student_affairs_pdf_urls[i])
    resp.raise_for_status()  # 若失敗會拋出例外

    with open(f'{out_dir}/student_affairs_{i+1}.pdf', 'wb') as f:
        f.write(resp.content)