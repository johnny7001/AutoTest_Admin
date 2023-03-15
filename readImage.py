import pytesseract
from PIL import Image

filepath = 'captcha.png'

def getCaptcha(filepath):
    try:
        pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract.exe"
        img = Image.open(filepath)
        # img.show()
        # 處理圖片array
        imgResult = pytesseract.image_to_string(img, lang="eng").strip() # type=str
        return imgResult
    except Exception as err:
        print(err)
        return f"識別失敗, 錯誤訊息: {err}"

number = getCaptcha(filepath)
print(number)