from .models import *
from .serializers import *

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class UsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # 인스턴스 없으면 생성해서 가져옴
        us_instance, _ = Us.objects.get_or_create(user=user)
        serializer = UsSerializer(us_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
