# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxLengthValidator

"""
닉네임: username
아이디: userid
"""

class User(AbstractUser):
    username = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[0-9a-zA-Z가-힣]*$',
                message='닉네임은 한글, 영어, 숫자만 사용할 수 있습니다.'
            )
        ]
    )

    userid = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',  # 허용할 문자 및 숫자 정의
                message='50자 이하 문자, 숫자 그리고 @/./+/-/_만 가능합니다.',
                code='invalid_userid'
            )
        ]
    )


