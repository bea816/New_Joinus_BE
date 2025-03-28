from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response

# 회원가입 뷰
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "회원가입에 실패했습니다.",
                "errors": serializer.errors
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
                "message": "사용할 수 없는 닉네임입니다.",
                "errors": serializer.errors
            }, status=status.HTTP_202_ACCEPTED)
