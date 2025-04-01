from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.db import IntegrityError # 회원가입 userid 길이
from rest_framework.permissions import IsAuthenticated # 로그인 확인

# 회원가입 뷰
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)  
            user = serializer.save()  
            token = Token.objects.create(user=user) 
            return Response({
                "user": {
                    'username': user.username,
                    'userid': user.userid,
                },
                "token": token.key  
            }, status=status.HTTP_200_OK)
        # 규정 내 회원가입 실패
        except ValidationError as e:
            return Response({
                "message": "회원가입에 실패했습니다.",
                "errors": e.detail  
            }, status=status.HTTP_202_ACCEPTED)  
        # userid 길이 초과
        except IntegrityError as e:
            if "Data too long for column 'userid'" in str(e):
                return Response({
                    "message": "회원가입에 실패했습니다.",
                    "errors": "아이디는 50자를 초과할 수 없습니다."
                }, status=status.HTTP_400_BAD_REQUEST)
        # 규정 이외 회원가입 실패
        except Exception as e:
            return Response({
                "message": "알 수 없는 오류가 발생했습니다.",
                "details": str(e)  
            }, status=status.HTTP_202_ACCEPTED)

# 닉네임 중복 확인 뷰
class UsernameUniqueView(generics.GenericAPIView):
    serializer_class = UsernameUniqueSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": "사용 가능한 닉네임입니다."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "사용할 수 없는 닉네임입니다."
            }, status=status.HTTP_202_ACCEPTED)

# 로그인
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        # 유효성 검사
        if not serializer.is_valid():
            return Response({
                "errors": serializer.errors,
                "message": "로그인에 실패했습니다."
            }, status=status.HTTP_202_ACCEPTED)

        token = serializer.validated_data['token']
        return Response({"token": token}, status=status.HTTP_200_OK)

# 로그아웃 뷰
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            Token.objects.get(user=request.user).delete()  # 토큰 삭제
            return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"message": "토큰이 존재하지 않습니다."}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"message": "로그아웃에 실패했습니다.", "details": str(e)}, status=status.HTTP_202_ACCEPTED)

class UsernameUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"current_username": user.username}, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UsernameUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # 🔥 직접 user.username을 업데이트한 후 저장
            user.username = serializer.validated_data['username']
            user.save(update_fields=['username'])  # 변경된 필드만 저장

            return Response({"message": "닉네임이 변경되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)