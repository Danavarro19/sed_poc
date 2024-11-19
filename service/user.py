from data.model import User, Session
from datetime import datetime, timedelta, timezone
import secrets
import bcrypt


def signup_service(**data):
    data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    data['role'] = 'user'
    user = User(**data)
    user.save()


def signin_service(username, password):
    user = User.objects.select_by_field("username", username)
    if not user:
        raise Exception("User not found")

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise Exception("Invalid password")

    token = secrets.token_hex(32)
    created_at = datetime.now(tz=timezone.utc)
    expires_at = created_at + timedelta(minutes=30)
    session = Session(
        user_id=user.user_id,
        session_token=token,
        created_at=created_at,
        expires_at=expires_at
    )
    session.save()
    return token, expires_at


def signout_service(token):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    session = Session.objects.select_by_field("session_token", token)
    Session.objects.update(session.session_id, {'expires_at': datetime.now(tz=timezone.utc).strftime(date_format)})


def validate_session(token):
    session = Session.objects.select_by_field("session_token", token)
    if not session or session.revoked:
        return None
    user = User.objects.select_by_pk(session.user_id, field_names=['username', 'email', 'role'])
    return user
