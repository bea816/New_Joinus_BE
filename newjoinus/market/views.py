from .models import *
from .serializers import *
from users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404

"""
광고와 아이템은 admin에서 등록하면 됨
아이템의 note 필드는 admin에서 등록하지 않고 빈칸으로 두면 됨
"""

# 아이템 리스트
class ItemListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()
        user = request.user

        item_serializer = ItemListSerializer(items, many=True, context={'request': request})
        userpoint_serializer = UserPointsSerializer(user)

        return Response({
            **userpoint_serializer.data, 
            "item": item_serializer.data
            }, status=status.HTTP_200_OK)

# 아이템 디테일
class ItemDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        items = get_object_or_404(Item, id=pk)
        item_serializer = ItemDetailSerializer(items, context={'request': request})

        user = request.user
        userpoint_serializer = UserPointsSerializer(user)

        # 구매 여부 확인
        purchased = Purchase.objects.filter(user=user, item=items).exists()
        
        button_text = "구매하기"
        if purchased:
            if items.item_type == "sticker":
                button_text = "다운받기"
            else:
                button_text = "구매 완료"

        return Response({
            **userpoint_serializer.data, # 딕셔너리 언패킹
            **item_serializer.data,
            "button_text": button_text
        }, status=status.HTTP_200_OK)

    def post(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        serializer = PurchaseSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "구매가 완료되었습니다."}, status=status.HTTP_200_OK)
            except serializers.ValidationError as e:
                return Response({"message": e.detail[0]}, status=status.HTTP_202_ACCEPTED) # 에러 메세지만 출력

        """
        # 에러 메세지만 출력
        error_messages = [str(msg[0]) for msg in serializer.errors.values()]
        return Response({"message": error_messages[0]}, status=status.HTTP_202_ACCEPTED)
        """
        return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)