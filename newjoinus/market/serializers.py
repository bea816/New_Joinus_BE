from rest_framework import serializers
from .models import *
from users.models import User

# 사용자 포인트
class UserPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["points"]

# 아이템 리스트
class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["item_name", "price", "id"]

# 아이템 디테일
class ItemDetailSerializer(serializers.ModelSerializer):
    note = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            "item_name",
            "price",
            "description",
            "note",
            "id"
            )

    # 타입별 노트
    def get_note(self, obj):
        if obj.item_type == "sticker":
            return "*다운받아 사용해주세요!"
        elif obj.item_type == "theme":
            return "*어스 오른쪽 상단의 메뉴 아이콘 클릭>어스테마 바꾸기 에서 테마 변경 가능합니다."
        else:  # "frame"
            return "*구매 시 바로 실천카드 프레임 고르기에서 적용 가능합니다."

# 아이템 구매
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['item']

    def create(self, validated_data):
        user = self.context['request'].user
        item = validated_data['item']

        # 이미 구매한 품목인지 확인
        if Purchase.objects.filter(user=user, item=item).exists():
            raise serializers.ValidationError("이 품목은 이미 구매하였습니다.")

        # 포인트 부족 체크
        if user.points < item.price:
            raise serializers.ValidationError("포인트가 부족합니다.")

        # 포인트 차감 및 저장
        user.points -= item.price
        user.save()

        purchase = Purchase.objects.create(user=user, item=item)
        return purchase