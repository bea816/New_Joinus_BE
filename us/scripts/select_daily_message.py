import os
import sys
import django
import random
from datetime import date, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Django 설정 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newjoinus.settings.local')
django.setup()

from us.models import DailyMessage, SelectedDailyMessage

def select_message():
    today = date.today()
    yesterday = today - timedelta(days=1)

    # 어제의 메시지
    yesterday_message = SelectedDailyMessage.objects.filter(date=yesterday).first()

    # 오늘 메시지가 이미 설정되어 있으면 아무것도 하지 않음
    if SelectedDailyMessage.objects.filter(date=today).exists(): 
        print("오늘의 메시지는 이미 존재합니다.")
        return

    messages = list(DailyMessage.objects.exclude(content="").values_list("content", flat=True))


    # 등록된 메시지 중에서 어제의 메시지 제외
    if yesterday_message:
        messages = [msg for msg in messages if msg != yesterday_message.message.content]

    if not messages:
        print("등록된 메시지가 없습니다.")
        return

    # 랜덤으로 메세지 선택
    message_content = random.choice(messages)

    selected_message = DailyMessage.objects.get(content=message_content)
    SelectedDailyMessage.objects.create(message=selected_message, date=today)
    print(f"'{message_content}' 메시지가 오늘의 메시지로 설정되었습니다.")

if __name__ == "__main__":
    select_message()