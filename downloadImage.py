from selenium.webdriver.common.by import By
import logging
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

# 下載圖片
def downloadImg(captchaBase64, filename):
    try:
        # 先將 data Url 前綴 (data:image/png;base64) 去除，再將 base64 資料轉為 bytes
        i = base64.b64decode(captchaBase64.split(',')[1])
        i = io.BytesIO(i)
        i = mpimg.imread(i, format='PNG') # 讀檔會失敗
        # # 顯示驗證碼
        plt.imshow(i)
        # 不顯示xy軸及邊框
        plt.axis('off')
        # plt.show()
        plt.savefig(f"./{filename}")
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

Account="Stage2000214"
Password="test1234"
AuthNO="53538851"

driver = open_driver()

driver.get('https://vendor-stage.ecpay.com.tw/MerchantBasicInfo/MerchantBasicInfo')
# 視窗最大化
# driver.maximize_window()
# 點我登入
driver.find_element(By.XPATH, '//*[@id="ecpayLogin"]').click()
# 輸入帳號
driver.find_element(By.XPATH, '//*[@id="Account"]').send_keys(Account)

# 判斷是否有彈跳視窗, 若有彈跳視窗表示登入失敗
# while True:
# 點選繼續
driver.find_element(By.XPATH, '//*[@id="LoginAllPay"]').click()
driver.implicitly_wait(10)
# 輸入密碼
driver.find_element(By.XPATH, '//*[@id="Password"]').send_keys(Password)
# 輸入統一編號
driver.find_element(By.XPATH, '//*[@id="AuthNO"]').send_keys(AuthNO)
filename = "captcha.png"

# 下載圖片
captchaBase64 = catchBase64(driver)
downloadImg(captchaBase64, filename)

ListCookies = driver.get_cookies()  # type = list
print('印出cookies: ')
print(ListCookies)
with open('./ImageCookies.txt', 'w') as f:
    f.write(str(ListCookies))
