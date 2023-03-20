from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import logging
import time
from pkg import AdminLogin, open_driver, cookieLogin, sendEmail

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename=f'autoTest_NoSemicolon.txt', filemode='a+', format=FORMAT,
                    encoding='utf-8')
# 紀錄信件內容
mailContent = ''
driver = open_driver()
# 登入後台
driver = AdminLogin(driver)
driver.implicitly_wait(30)
# 帶cookie進到廠商基本資料後拿到soup
soup = cookieLogin(driver)

# 顯示修改之前的電子信箱
while soup.find('input', id='ContactEmail') is None:
    print('沒抓到聯絡人信箱, 重新登入')
    driver = AdminLogin(driver)
    driver.implicitly_wait(30)
    soup = cookieLogin(driver)

contactEmail = soup.find('input', id='ContactEmail').get('value')
print(f'修改之前的電子信箱:{contactEmail}')
logging.info(f'修改之前的電子信箱:{contactEmail}')
mailContent += f'修改之前的電子信箱:{contactEmail}\n'

# 輸入的信箱
InputEmail = 'helloJapan@gmail.com'
# 修改帳務聯絡人電子信箱
driver.find_element(By.XPATH, '//*[@id="ContactEmail"]').send_keys(InputEmail)
print(f'輸入的電子信箱:{InputEmail}')
logging.info(f'輸入的電子信箱:{InputEmail}')
mailContent += f'輸入的電子信箱:{InputEmail}\n'
# 點擊修改
driver.find_element(By.XPATH, '//*[@id="btUpdata"]').click()
time.sleep(2)
# 判斷視窗是否有出現
try:
    alert = driver.switch_to.alert  # 定位談窗
    if alert.text != '如需設定多組信箱，中間請以半形分號區隔。':
        print(f'彈跳視窗回傳訊息: {alert.text}與工單要求不相符-Fail')
        logging.info(f'彈跳視窗回傳訊息: {alert.text}與工單要求不相符-Fail')
        mailContent += f'彈跳視窗回傳訊息: {alert.text}與工單要求不相符-Fail\n'
    else:
        print(f'彈跳視窗回傳訊息: {alert.text}-Pass')
        logging.info(f'彈跳視窗回傳訊息: {alert.text}-Pass')
        mailContent += f'彈跳視窗回傳訊息: {alert.text}-Pass\n'
    driver.switch_to.alert.accept()  # 點擊確定按鈕
except Exception as err:
    logging.info(f'未出現彈跳視窗訊息: {err}')
    mailContent += f'未出現彈跳視窗訊息: {err}\n'

# 重新整理頁面
driver.refresh()
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')
while soup.find('input', id='ContactEmail') is None:
    print('沒抓到聯絡人信箱, 重新整理頁面')
    # 重新登入
    driver = AdminLogin(driver)
    driver.implicitly_wait(30)
    soup = cookieLogin(driver)

editContactEmail = soup.find('input', id='ContactEmail').get('value')
print(f'檢查信箱內容是否有被更修改:{editContactEmail}')
logging.info(f'檢查信箱內容是否有被更修改:{editContactEmail}')
mailContent += f'檢查信箱內容是否有被更修改:{editContactEmail}\n'
if contactEmail == editContactEmail:
    print('信箱內容未被修改-Pass')
    logging.info('信箱內容未被修改-Pass')
    mailContent += '信箱內容未被修改-Pass\n'
else:
    print('信箱內容已被修改,請檢查是否異常-Fail')
    logging.info('信箱內容已被修改,請檢查是否異常-Fail')
    mailContent += '信箱內容已被修改,請檢查是否異常-Fail\n'
logging.info("="*150)
driver.close()
# 寄信通知結果
sendEmail(mailTitle='autoTest_NoSemicolon', mailContent=mailContent)