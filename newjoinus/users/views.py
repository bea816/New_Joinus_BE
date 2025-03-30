from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
#from rest_framework.authtoken.models import Token

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
        except ValidationError as e:
            return Response({
                "message": "회원가입에 실패했습니다.",
                "errors": e.detail  
            }, status=status.HTTP_202_ACCEPTED)  
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
