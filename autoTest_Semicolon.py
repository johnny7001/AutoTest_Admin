from bs4 import BeautifulSoup
import logging
import time
from pkg import open_driver,AdminLogin,cookieLogin
from selenium.webdriver.common.by import By

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename=f'autoTest_Semicolon.txt', filemode='a+', format=FORMAT,
                    encoding='utf-8')

driver = open_driver()
# 登入後台
driver = AdminLogin(driver)
driver.implicitly_wait(30)
# 帶cookie進到廠商基本資料後拿到soup
soup = cookieLogin(driver)

# 顯示修改之前的電子信箱
while soup.find('input',id='ContactEmail') is None:
    print('沒抓到聯絡人信箱, 重新登入')
    # 重新登入
    driver = AdminLogin(driver)
    driver.implicitly_wait(30)
    soup = cookieLogin(driver)

contactEmail = soup.find('input', id='ContactEmail').get('value')
print(f'修改之前的電子信箱:{contactEmail}')
logging.info(f'修改之前的電子信箱:{contactEmail}')

# 產生隨機碼
mailRandomNum = str(int(time.time()))
# 輸入的信箱
InputEmail = f'{mailRandomNum}@ecpay.com.tw;helloJapan@gmail.com'
# 清除修改前的信箱內容
driver.find_element(By.XPATH, '//*[@id="ContactEmail"]').clear()
# 修改帳務聯絡人電子信箱
driver.find_element(By.XPATH, '//*[@id="ContactEmail"]').send_keys(InputEmail)
print(f'輸入的電子信箱:{InputEmail}')
logging.info(f'輸入的電子信箱:{InputEmail}')
# 點擊修改
driver.find_element(By.XPATH, '//*[@id="btUpdata"]').click()
time.sleep(2)
# 判斷視窗是否有出現
try:
    alert = driver.switch_to.alert  # 定位談窗
    if alert.text != '更新成功':
        print(f'彈跳視窗回傳訊息: {alert.text},請檢查是否異常-Fail')
        logging.info(f'彈跳視窗回傳訊息: {alert.text},請檢查是否異常-Fail')
    else:
        print(f'彈跳視窗回傳訊息: {alert.text}-Pass')
        logging.info(f'彈跳視窗回傳訊息: {alert.text}-Pass')
    driver.switch_to.alert.accept()  # 點擊確定按鈕
except Exception as err:
    logging.info(f'未出現彈跳視窗訊息: {err}')

# 重新整理頁面
driver.refresh()
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')
while soup.find('input',id='ContactEmail') is None:
    print('沒抓到聯絡人信箱, 重新整理頁面')
    # 重新登入
    driver = AdminLogin(driver)
    driver.implicitly_wait(30)
    soup = cookieLogin(driver)

editContactEmail = soup.find('input', id='ContactEmail').get('value')
print(f'檢查信箱內容是否有被更修改:{editContactEmail}')
logging.info(f'檢查信箱內容是否有被更修改:{editContactEmail}')
if contactEmail == editContactEmail:
    print('信箱內容未被修改,請檢查是否異常-Fail')
    logging.info('信箱內容未被修改,請檢查是否異常-Fail')
else:
    print('信箱內容更新成功-Pass')
    logging.info('信箱內容更新成功-Pass')
logging.info("="*150)
driver.close()
