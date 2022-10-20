import smtplib
from email.message import EmailMessage

from config import config


class Gmail:
    @staticmethod
    def send(subject: str, content: str, to: str = "vl.strugatsky@gmail.com"):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = config.gmail['account']
        msg['To'] = to
        msg.set_content(content)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(config.gmail['account'], config.gmail['app_password'])
            smtp.send_message(msg)


if __name__ == '__main__':
    Gmail.send('test message', 'body of the test message')
