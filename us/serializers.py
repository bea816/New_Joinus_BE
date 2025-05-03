from rest_framework import serializers
from .models import *
from market.models import Item, Purchase
from market.serializers import ItemListSerializer

class UsSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    points = serializers.IntegerField(source='user.points', read_only=True)
    available_items = serializers.SerializerMethodField()
    current_theme = serializers.ReadOnlyField(source='user.current_theme')
    daily_message = serializers.SerializerMethodField()
    #total_cards = serializers.SerializerMethodField() # 총 누적된 카드 개수

    class Meta:
        model = Us
        fields = ("username", "current_theme", "points", "daily_message", "available_items")
        
        # "total_cards", "my_lank", "comment"

    #def get_total_cards(self, obj):
    #    return CardPost.objects.filter(author=obj.user).count()

    # 마켓에서 구매 가능한 아이템
    def get_available_items(self, obj):
        user = obj.user
        user_points = user.points

        # 사용자가 이미 구매한 아이템 목록
        purchased_ids = Purchase.objects.filter(user=user).values_list('item__id', flat=True)
        items_not_purchased = Item.objects.exclude(id__in=purchased_ids)

        # 구매하지 않은 아이템 중 최대 4개
        buyable_items = items_not_purchased.filter(price__lte=user_points)[:4]

        return ItemListSerializer(buyable_items, many=True).data
    
    def get_daily_message(self, obj):
        from datetime import date
        today = date.today()
        selected = SelectedDailyMessage.objects.filter(date=today).first()
        return selected.message.content if selected else "당신이 있어서 세상이 더 아름다워요."