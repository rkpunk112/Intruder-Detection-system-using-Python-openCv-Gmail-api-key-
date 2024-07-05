import smtplib
from email.message import EmailMessage
import imghdr
password = "" ##API_KEY_OF_UR_GMAIL_ACC
sendr="" ##SENDER_EMAIL_ID
recv="" ##RECEIVER_EMAIL_ID
def send_email(img_path):
    email_msg=EmailMessage()
    email_msg["Subject"]= "New intruder Showed upp"
    email_msg.set_content("Hey we have a new Intruder here are the images")

    with open(img_path,"rb") as file:
        content= file.read()
    email_msg.add_attachment(content,maintype="image",subtype=imghdr.what(None,content))

    gmail=smtplib.SMTP("smtp.gmail.com",587)
    ##starting the Email server parameter
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sendr,password)
    gmail.sendmail(sendr,recv,email_msg.as_string())
    gmail.quit()




