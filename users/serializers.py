from .models import *
from market.models import Purchase, Item

from django.contrib.auth.password_validation import validate_password # 패스워드 검증
from django.contrib.auth import authenticate # user 인증함수. 자격증명 유효한 경우 User객체 반환
from rest_framework import serializers
from rest_framework.authtoken.models import Token # 토큰 모델
from rest_framework.validators import UniqueValidator # 이메일 중복방지 검증
from django.contrib.auth import authenticate # 로그인 사용자 인증
from rest_framework.exceptions import ValidationError
import re
from django.contrib.auth import get_user_model

# 회원가입 비밀번호 조건
def validate_password_strength(password):
    if not re.search(r'\d', password):
        raise ValidationError(
            "비밀번호는 최소 1개 이상의 숫자를 포함해야 합니다.",
            code='password_no_number'
        )

# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    # 닉네임
    username = serializers.CharField(
        required=True,
        validators= [
            UniqueValidator(queryset=User.objects.all(), message="이미 사용 중인 닉네임입니다."),
            ]
    )

    # 아이디
    userid = serializers.CharField(
        required = True,
        validators = [
            UniqueValidator(queryset=User.objects.all(), message="이미 사용 중인 아이디입니다."),
            ]
    )

    password = serializers.CharField(
        write_only = True,
        required = True,
        validators=[validate_password, validate_password_strength] # 비밀번호 검증

    )

    password2 = serializers.CharField(
        write_only = True,
        required = True) 

    class Meta:
        model = User
        fields = ['username', 'userid', 'password', 'password2']

    # 닉네임 확인 response
    def validate_username(self, value):
        if not re.match(r'^[0-9a-zA-Z가-힣]+$', value):
            raise serializers.ValidationError("닉네임은 한글, 영어, 숫자만 사용할 수 있습니다.")

        if len(value) > 8:
            raise serializers.ValidationError("닉네임은 8자를 초과할 수 없습니다.")
        return value

    def validate_userid(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("아이디는 50자를 초과할 수 없습니다.")

        # 아이디 중복 확인
        if User.objects.filter(userid=value).exists():
            raise serializers.ValidationError("이 아이디는 이미 사용 중입니다.")
        
        # 문자가 포함되어 있는지 확인
        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError("아이디는 최소 1개 이상의 문자를 포함해야 합니다.")
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
    
    # 유저 생성 / 토큰은 뷰에서 생성
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            userid=validated_data['userid'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # 토큰 생성은 뷰에서 처리하도록 변경
        return user

# 닉네임 중복 확인 시리얼라이저
class UsernameUniqueSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators= [UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username']

# 로그인 시리얼라이저
class LoginSerializer(serializers.Serializer):
    userid = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        User = get_user_model()

        try:
            user = User.objects.get(userid=data['userid'])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"error": "잘못된 아이디/비밀번호입니다."}
            )
        
        if user.check_password(data['password']):
            token, created = Token.objects.get_or_create(user=user)
            return {
                'token': token.key,  
                'user': user  
            }
        raise ValidationError({"error": "잘못된 아이디/비밀번호입니다."}) 

# 로그아웃 시리얼라이저
class LogoutSerializer(serializers.Serializer):
    pass  # 별도의 필드 필요 없음

# 회원정보 수정 시리얼라이저
class UsernameUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="이미 사용 중인 닉네임입니다.")
        ]
    )

    class Meta:
        model = User
        fields = ['username']

    def validate_username(self, value):
        if not re.match(r'^[0-9a-zA-Z가-힣]+$', value):
            raise serializers.ValidationError("닉네임은 한글, 영어, 숫자만 사용할 수 있습니다.")

        if len(value) > 8:
            raise serializers.ValidationError("닉네임은 8자를 초과할 수 없습니다.")
        return value    

    def update(self, instance, validated_data):
        new_username = validated_data.get('username', instance.username)

        if instance.username != new_username:  # 변경 사항이 있는 경우만 업데이트
            instance.username = new_username
            instance.save(update_fields=['username'])

        return instance

# 구매내역 시리얼라이저
class OrderListSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item_name')
    price = serializers.IntegerField(source='item.price')

    class Meta:
        model = Purchase
        fields = ['item_name', 'price']

# 테마 조회, 변경 시리얼라이저
class CurrentThemeSerializer(serializers.Serializer): 
    change_theme = serializers.CharField(write_only=True)  
    current_theme = serializers.CharField(read_only=True)  

    def validate_change_theme(self, value):
        user = self.context['request'].user

        # 기본 테마는 누구나 선택 가능
        if value == "기본 테마":
            return value

        # 구매한 테마인지 확인
        purchased_themes = Purchase.objects.filter(
            user=user, item__item_type="theme"
        ).values_list('item__item_name', flat=True)

        if value not in purchased_themes:
            raise serializers.ValidationError("구매한 테마만 변경할 수 있습니다.")

        return value

    def update(self, instance, validated_data):
        new_theme = validated_data.get('change_theme', instance.current_theme)  
        instance.current_theme = new_theme
        instance.save()
        return instance