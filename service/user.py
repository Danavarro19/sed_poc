from data.model import User, Session
from datetime import datetime, timedelta
import secrets
import bcrypt


def signup_service(**data):
    data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(**data)
    user.save()


def signin_service(username, password):
    user = User.objects.select_by_field("username", username)
    if not user:
        raise Exception("User not found")

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise Exception("Invalid password")

    token = secrets.token_hex(32)
    created_at = datetime.now()
    session = Session(
        user_id=user.user_id,
        session_token=token,
        created_at=created_at,
        expires_at=created_at + timedelta(minutes=30)
    )
    session.save()
    return token


def validate_session(token):
    session = Session.objects.select_by_field("session_token", token)
    if not session or session.revoked:
        return None
    user = User.objects.select_by_pk(session.user_id, field_names=['username', 'email'])
    return user
