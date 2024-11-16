from data.model import User


def signup_service(**data):
    user = User(**data)
    user.save()
