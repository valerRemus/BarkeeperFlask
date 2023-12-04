from app import db
from . import messagess
from .forms import MessageForm
from app.models import User, Message
from flask_login import login_required, current_user
from flask import redirect, url_for, render_template, flash
from flask_babel import gettext
from werkzeug.exceptions import abort


@messagess.route('/messages', methods=['GET','POST'])
@login_required
def messages():
    return render_template('messages/messages.html', user=current_user)

@messagess.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    form = MessageForm()
    if form.validate_on_submit():
        sender_username = form.sender_username.data
        receiver_username = form.receiver_username.data
        content = form.content.data

        sender = User.query.filter_by(username=sender_username).first()
        receiver = User.query.filter_by(username=receiver_username).first()

        if sender and receiver:
            message = Message(sender_id=sender.id, receiver_id=receiver.id, content=content)
            db.session.add(message)
            db.session.commit()

            flash(gettext('The message have been sent!'))
            return redirect(url_for('messagess.messages'))

    return render_template('messages/send_message.html', form=form)

@messagess.route('/messagess/<int:message_id>')
@login_required
def message_details(message_id):
    message = Message.query.get_or_404(message_id)

    if not message.read:
        message.read = True
        db.session.commit()
    return render_template('messages/message_details.html', message=message)

@messagess.route('/receivedmessages')
@login_required
def received_messages():
    user = User.query.get(current_user.id)
    received_messages = user.received_messages

    return render_template('messages/received_messages.html', messages=received_messages)


@messagess.route('/messagess/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)

    if current_user != message.receiver:
        abort(403)

    db.session.delete(message)
    db.session.commit()

    flash(gettext('Message deleted successfully.'))

    return redirect(url_for('messagess.received_messages'))