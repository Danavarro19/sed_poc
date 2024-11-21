import hashlib

import psycopg2

from data.model import User, Session
from datetime import datetime, timedelta, timezone
import secrets
import bcrypt
import re

from data.orm.manager import Filter
from exception import ValidationException, AuthenticationException


def signup_service(**data):
    if not is_password_valid(data['password']):
        raise ValidationException('Contraseña debil')
    data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    data['role'] = 'user'
    user = User(**data)
    try:
        user.save()
    except psycopg2.errors.UniqueViolation:
        raise ValidationException('Campos duplicados.')


def signin_service(username, password):
    user = User.objects.select_by_field("username", username)
    if not user:
        raise AuthenticationException("User not found")

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise AuthenticationException("Invalid password")

    session_token = secrets.token_hex(32)
    csrf_token = secrets.token_urlsafe(32)
    created_at = datetime.now(tz=timezone.utc)
    expires_at = created_at + timedelta(minutes=30)
    session = Session(
        user_id=user.user_id,
        session_token=_hash_token(session_token),
        csrf_token=csrf_token,
        created_at=created_at,
        expires_at=expires_at
    )
    session.save()
    return session_token, expires_at


def signout_service(token):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    session = Session.objects.select_by_field("session_token", _hash_token(token))
    Session.objects.update(session.session_id, {'expires_at': datetime.now(tz=timezone.utc).strftime(date_format)})


def validate_session(token):
    session = Session.objects.select_by_field("session_token", _hash_token(token))
    if not session or session.revoked:
        return None, None
    user = User.objects.select_by_pk(session.user_id, field_names=['username', 'email', 'role'])
    return user, session


def _hash_token(token):
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def is_password_valid(password: str) -> bool:
    if len(password) < 8 or len(password) > 16:
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[0-9]', password):
        return False

    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]', password):
        return False

    return True


def get_users():
    filters = [Filter(field='role', value='super', criteria='!=')]
    return User.objects.select(field_names=['user_id', 'username', 'email', 'role'], filter_by=filters)


def update_user_role(key, data):
    if len(data.values()) > 1 or list(data.keys())[0] != 'role':
        raise ValidationException("Invalid data")

    if data['role'] not in ['admin', 'user']:
        raise ValidationException("Invalid role")
    User.objects.update(key, data)
