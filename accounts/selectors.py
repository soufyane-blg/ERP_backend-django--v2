from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_by_username(username: str):
    return User.objects.filter(username=username).first()


def get_user_by_id(user_id: int):
    return User.objects.filter(id=user_id).first()