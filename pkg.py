from email.mime.text import MIMEText
import smtplib
from datetime import datetime, timezone, timedelta
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
import pytesseract
from PIL import Image
import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import time
from bs4 import BeautifulSoup
# from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1600, 900))
display.start()
# load_dotenv()
# Account = os.getenv("Account")
# Password = os.getenv("Password")
# AuthNO = os.getenv("AuthNO")

# from apscheduler.schedulers.blocking import BlockingScheduler


def message(msg):
    # - |2017-04-09 02:08:55.764256 | 訊息，顯示在這邊
    current = '{0:%Y-%m-%d %H:%M:%S.%f}'.format(
        datetime.now(timezone.utc) + timedelta(hours=8))
    log = "- |" + current + " | " + ": " + str(msg)
    print(log)
    return log

# 執行chrome_driver


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
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        # 設置修改selenium的特徵值, 防止被偵測
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        # GithubAction用
        chrome_options.add_argument('--window-size=1200,1200')
        chrome_options.add_argument('--ignore-certificate-errors')

        # driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        return driver
    except Exception as err:
        logging.info(f'chrome_diver開啟失敗, 錯誤碼: {err}')

# 辨識圖片


def getCaptcha(filepath):
    try:
        # now_path = os.getcwd()  # 查看現在在哪一個路徑
        # PATH = now_path + r"\Tesseract-OCR\tesseract.exe"
        # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        pytesseract.pytesseract.tesseract_cmd = "./Tesseract-OCR/tesseract.exe"
        img = Image.open(filepath)
        print('開啟圖檔準備辨識： '+img)
        # img.show()
        imgResult = pytesseract.image_to_string(
            img, lang="eng").strip()  # type=str
        print('辨識碼結果：', imgResult, type(imgResult))
        return imgResult
    except Exception as err:
        return logging.info(f"識別失敗, 錯誤訊息: {err}")

# 下載圖片


def downloadImg(captchaBase64, filename):
    try:
        # 先將 data Url 前綴 (data:image/png;base64) 去除，再將 base64 資料轉為 bytes
        i = base64.b64decode(captchaBase64.split(',')[1])
        i = io.BytesIO(i)
        i = mpimg.imread(i, format='PNG')  # 讀檔會失敗
        print('array:'+i)
        # # 顯示驗證碼
        plt.imshow(i)
        # 不顯示xy軸及邊框
        plt.axis('off')
        # plt.show()
        plt.savefig(filename)
        print(f'{filename}圖片下載')
    except Exception as err:
        logging.info(f'圖片讀檔失敗, 錯誤訊息: {err}')

# 用js處理base64


def catchBase64(driver):
    try:
        # 用js處理圖片
        captchaBase64 = driver.execute_async_script("""
            var canvas = document.createElement('canvas');
            var context = canvas.getContext('2d');
            var img = document.querySelector('#code');
            canvas.height = img.naturalHeight;
            canvas.width = img.naturalWidth;
            context.drawImage(img, 0, 0);

            callback = arguments[arguments.length - 1];
            callback(canvas.toDataURL());
            """)
        print("處理js圖片")
        return captchaBase64
    except Exception as err:
        logging.info(f'catchBase64失敗, 錯誤訊息: {err}')


# Account = "Stage2000214"
# Password = "test1234"
# AuthNO = "53538851"

# 後台登入


def AdminLogin(driver):
    driver.get(
        'https://vendor-stage.ecpay.com.tw/MerchantBasicInfo/MerchantBasicInfo')
    # 視窗最大化
    # driver.maximize_window()
    # 點我登入
    driver.find_element(By.XPATH, '//*[@id="ecpayLogin"]').click()
    # 輸入帳號
    driver.find_element(
        By.XPATH, '//*[@id="Account"]').send_keys("Stage2000214")

    # 判斷是否有彈跳視窗, 若有彈跳視窗表示登入失敗
    while True:
        # 點選繼續
        driver.find_element(By.XPATH, '//*[@id="LoginAllPay"]').click()
        driver.implicitly_wait(10)
        # 輸入密碼
        driver.find_element(
            By.XPATH, '//*[@id="Password"]').send_keys("test1234")
        # 輸入統一編號
        driver.find_element(
            By.XPATH, '//*[@id="AuthNO"]').send_keys("53538851")
        filename = "captcha.png"

        captchaBase64 = catchBase64(driver)
        downloadImg(captchaBase64, filename)
        time.sleep(1)
        imgOpen = Image.open(filename)
        print(imgOpen.size)
        print(imgOpen.mode)
        # 處理圖片, 取得驗證碼
        number = getCaptcha(filename)
        print(f'取得驗證碼: {number}')

        while number.isdigit() != True or len(number) < 4:
            # 點擊驗證碼圖案, 更換後驗證碼後驗證新的驗證碼
            driver.find_element(By.XPATH, '//*[@id="code"]').click()
            time.sleep(1)
            # 重新下載新的驗證碼
            captchaBase64 = catchBase64(driver)
            downloadImg(captchaBase64, filename)
            time.sleep(1)
            # 重新處理驗證碼
            number = getCaptcha(filename)
            print(f'新的驗證碼:{number}')
            time.sleep(1)

        # 輸入驗證碼
        driver.find_element(
            By.XPATH, '//*[@id="allpayCaptchaValue"]').send_keys(number)
        # 點擊登入
        driver.find_element(By.XPATH, '//*[@id="LoginAllPay"]').click()
        time.sleep(2)
        try:
            alert = driver.switch_to.alert  # 定位談窗
            print(f'彈跳視窗訊息: {alert.text}')
            driver.switch_to.alert.accept()  # 點擊確定按鈕
        except:
            print('登入成功')
            break
    return driver

# 保存cookie且登入


def cookieLogin(driver):
    # 保存cookie
    ListCookies = driver.get_cookies()  # type = list
    for cookie in ListCookies:
        driver.add_cookie(cookie)
    driver.get(
        'https://vendor-stage.ecpay.com.tw/MerchantBasicInfo/MerchantBasicInfo')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def sendEmail():
    # SMTP
    account = "theforeverwen@gmail.com"
    password = "tcgfcyvjqvebwtcz"

    # 收信寄信人的資料
    to_email = "johnny.tseng@ecpay.com.tw"
    from_email = "theforeverwen@gmail.com"

    # MIME
    subject = "測試信件"
    send_message = "哈囉可以了嗎"
    msg = MIMEText(send_message, "html")
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    # 寄信
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(account, password)
    server.send_message(msg)
    server.quit()

# # 下載圖片
# def downloadImg(imgUrl):
#     try:
#
#         # 下載圖片
#         img = requests.get(url=imgUrl, stream=True, verify=False)
#         with open(r"CAPTCHA.jfif", "wb") as file:
#             file.write(img.content)
#         return message("圖片下載成功")
#     except:
#         return message("圖片下載失敗")

# # 若讀檔失敗,重新讀檔
# imageResult = downloadImg(filename) # return ImageSuccess or ImageError
# message(imageResult)
# while imageResult != 'ImageSuccess':
#     message("讀檔失敗,重新下載圖片")
#     # 點擊驗證碼圖案, 更換後驗證碼後驗證新的驗證碼
#     driver.find_element(By.XPATH, '//*[@id="code"]').click()
#     imageResult = downloadImg(filename)

# if __name__=='__main__':
#     main()
    # scheduler = BlockingScheduler(timezone="Asia/Taipei")
    # # 設定每週一到日上午9:30分自動爬取並更新資料庫
    # scheduler.add_job(main, 'cron', day_of_week='0-6', hour=14, minute=00)
    # scheduler.start()
