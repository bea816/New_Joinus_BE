from .models import *
from django.contrib.auth.password_validation import validate_password # 패스워드 검증
from django.contrib.auth import authenticate # user 인증함수. 자격증명 유효한 경우 User객체 반환

from rest_framework import serializers
from rest_framework.authtoken.models import Token # 토큰 모델
from rest_framework.validators import UniqueValidator # 이메일 중복방지 검증

# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    # 닉네임
    username = serializers.CharField(
        required=True,
        validators= [
            UniqueValidator(queryset=User.objects.all()),
            ]
    )

    # 아이디
    userid = serializers.CharField(
        required = True,
        validators = [
            UniqueValidator(queryset=User.objects.all()),
            ]
    )

    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password] # 비밀번호 검증

    )

    password2 = serializers.CharField(
        write_only = True,
        required = True) 

    class Meta:
        model = User
        fields = ['username', 'userid', 'password', 'password2']

    # 닉네임 글자 수 확인 response
    def validate_username(self, value):
        if len(value) > 8:
            raise serializers.ValidationError("닉네임은 8자를 초과할 수 없습니다.")
        return value

    # 아이디 중복 확인 response
    def validate_userid(self, value):
        if User.objects.filter(userid=value).exists():
            raise serializers.ValidationError("이 아이디는 이미 사용 중입니다.")
        return value    
    
    # 비밀번호 확인 response
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
        )

        # 비밀번호에 대한 추가 검사
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return data
    
    # 유저, 토큰 생성
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            userid=validated_data['userid'],
        )

        user.set_password(validated_data['password'])
        user.save()

        token = Token.objects.create(user=user)

        return {
            'user': user,
            'token': token.key
        }

# 닉네임 중복 확인 시리얼라이저
class UsernameUniqueSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators= [UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username']