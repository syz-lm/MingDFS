import smtplib
from email.header import Header
from email.mime.text import MIMEText
from logging import Logger

LOGGER = Logger(__name__)


def send_text_email(host, port, username, password, sender, receivers,
                    subject, FROM, to, content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(FROM, 'utf-8')
    message['To'] = Header(to, 'utf-8')

    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp_conn = smtplib.SMTP_SSL(host, port)
        smtp_conn.login(username, password)
        smtp_conn.sendmail(sender, receivers, message.as_string())
        return 1
    except smtplib.SMTPException as e:
        LOGGER.error(str(e))
        return -1
    finally:
        if smtp_conn: smtp_conn.close()
