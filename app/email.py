from threading import Thread

# I dont know why it raises circular error if i import them here so i imported them in the function

def send_async_email(app, msg):
    from . import mail
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    from flask import current_app, render_template
    from flask_mail import Message
    app = current_app._get_current_object()
    msg = Message(app.config['BARKEEPER_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['BARKEEPER_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

