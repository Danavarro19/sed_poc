from data.model import User


def signup_service(**data):
    user = User(**data)
    user.save()


def signin_service(username, password):
    user = User.objects.select_by_field("username", username)
    if user.password != password:
        raise Exception
    return user
