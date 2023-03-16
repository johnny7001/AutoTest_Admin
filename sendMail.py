from email.mime.text import MIMEText
import smtplib
def sendEmail():
    # SMTP
    account = "theforeverwen@gmail.com"
    password = "tcgfcyvjqvebwtcz"

    # 收信寄信人的資料
    # to_email = "johnny.tseng@ecpay.com.tw"
    to_email = "johnnytseng7001@gmail.com"
    from_email = "theforeverwen@gmail.com"

    # MIME
    subject = "測試信件"
    send_message = "哈囉可以了嗎"
    msg = MIMEText(send_message, "html")
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    # 寄信
    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=120)
    # server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.starttls()
    server.login(account, password)
    server.send_message(msg)
    server.quit()

sendEmail()
