import smtplib
import config


def send_mail(msg):
    if config.IS_TEST_CONFIG:
        pass
    else:

        to = ", ".join(config.ALARM_EMAILS_TO)
        body = "\r\n".join((
            "From: %s" % config.ALARM_EMAIL_FROM,
            "To: %s" % to,
            "Subject: TestCase failed",
            "",
            msg
        ))

        s = smtplib.SMTP(config.SMTP_HOST)
        s.sendmail(config.ALARM_EMAIL_FROM, config.ALARM_EMAILS_TO, body)
        s.quit()