from flask import render_template
from flask_mail import Message
from market import mail
from flask import current_app


def send_email(recipient, subject, template, **kwargs):
    app = current_app._get_current_object()
    with app.app_context():
        msg = Message(
            subject=app.config['EMAIL_SUBJECT_PREFIX'] + ' ' + subject,
            sender=app.config['EMAIL_SENDER'],
            recipients=[recipient])
        msg.html = render_template(template + '.html', **kwargs)
        msg.body = render_template(template + '.txt', **kwargs)
        mail.send(msg)
