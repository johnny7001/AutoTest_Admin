from selenium.webdriver.common.by import By
import logging
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import time
import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from selenium import webdriver
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1600, 900))
display.start()

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename=f'autoTest_NoSemicolon.txt', filemode='a+', format=FORMAT,
                    encoding='utf-8')

def open_driver():
    try:
        # Check if the current version of chromedriver exists
        chromedriver_autoinstaller.install()
        # and if it doesn't exist, download it automatically,
        # then add chromedriver to path

        # now_path = os.getcwd()  # 查看現在在哪一個路徑
        # PATH = now_path + "/chromedriver"
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless') # 無頭
        # chrome_options.add_experimental_option("detach", True)
        # 隱藏selenium的自動控制功能, 防止被偵測
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # 設置修改selenium的特徵值, 防止被偵測
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # GithubAction用
        chrome_options.add_argument('--window-size=1200,1200')
        chrome_options.add_argument('--ignore-certificate-errors')

        # driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        return driver
    except Exception as err:
        logging.info(f'chrome_diver開啟失敗, 錯誤碼: {err}')

def getCaptcha(filepath):
    try:
        pytesseract.pytesseract.tesseract_cmd = "./Tesseract-OCR/tesseract.exe"
        img = Image.open(f"{filepath}")
        # img.show()
        # 處理圖片array
        imgResult = pytesseract.image_to_string(img, lang="eng").strip() # type=str
        return imgResult
    except Exception as err:
        print(err)
        return logging.info(f"識別失敗, 錯誤訊息: {err}")

# 讀cookiess
with open('./ImageCookies.txt','r',encoding='utf-8') as file:
    content = file.read()
cookies = content.replace(']','').replace('[','')
print(cookies, type(cookies))
# driver = open_driver()
# driver.add_cookie(cookies)
# driver.get('https://vendor-stage.ecpay.com.tw/MerchantBasicInfo/MerchantBasicInfo')
# soup = BeautifulSoup(driver.page_source, 'html.parser')

# # 辨識圖片
# number = getCaptcha('/captcha.png')
# print(f'取得驗證碼: {number}')
#
# # 輸入驗證碼
# driver.find_element(By.XPATH, '//*[@id="allpayCaptchaValue"]').send_keys(number)
# # 點擊登入
# driver.find_element(By.XPATH, '//*[@id="LoginAllPay"]').click()
# time.sleep(2)
# try:
#     alert = driver.switch_to.alert  # 定位談窗
#     print(f'彈跳視窗訊息: {alert.text}')
#     driver.switch_to.alert.accept()  # 點擊確定按鈕
# except:
#     print('登入成功')
