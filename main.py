import time
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest

# اطلاعات ورود به حساب تلگرام
api_id = '22487790' 
api_hash = '09c24af20084de9372cc92a760c74961'      # API Hash خود را وارد کنید
phone_number = '+989369774231'  # شماره تلفن شما با کد کشور

# اتصال به حساب تلگرام
client = TelegramClient('session_name', api_id, api_hash)

def to_double_struck(text):
    double_struck_map = str.maketrans("0123456789:", "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡∶")
    return text.translate(double_struck_map)

async def update_name_with_time():
    async with client:
        while True:
            current_time = datetime.now().strftime('%H:%M')  # حذف ثانیه‌ها
            stylized_time = to_double_struck(current_time)
            custom_name = "𝒜𝐹𝒮𝐻𝐼𝒩  | "  # نام خود را اینجا وارد کنید
            new_name = f"{custom_name} {stylized_time}"
            await client(UpdateProfileRequest(first_name=new_name))
            print(f"Updated name to: {new_name}")

            # محاسبه زمان باقی‌مانده تا دقیقه بعد
            now = datetime.now()
            next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
            sleep_time = (next_minute - now).total_seconds()
            time.sleep(sleep_time)

with client:
    client.start(phone=phone_number)  # شروع و ورود به حساب
    client.loop.run_until_complete(update_name_with_time())
