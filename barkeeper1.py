import os

from app.messagess import messagess
from flask_login import current_user
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Message

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

@messagess.context_processor
def unread_messages_count():
    def get_unread_messages_count():
        if current_user.is_authenticated:
            count = Message.query.filter_by(receiver_id=current_user.id, read=False).count()
            return count
        return 0
    return dict(unread_messages_count=get_unread_messages_count)

app.context_processor(unread_messages_count)
