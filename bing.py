import requests
import os
import random
from variables import bot_url, chat_id, log_channel_id

# --- تنظیمات ---
IMAGE_TOPICS = ["forest", "mountain", "nature", "river", "waterfall"]  # موضوعات عکس

def main():
    os.chdir(os.path.realpath(os.path.dirname(__file__)))  # تغییر مسیر به مسیر فایل

    # انتخاب موضوع رندوم برای عکس
    topic = random.choice(IMAGE_TOPICS)
    imageUrl = f"https://source.unsplash.com/1920x1080/?{topic}"
    filename = "wallpaper.jpg"

    try:
        # دانلود تصویر
        r = requests.get(imageUrl)
        if "image" in r.headers.get("Content-Type", ""):
            with open(filename, "wb") as f:
                f.write(r.content)
            print("Image downloaded successfully")
        else:
            log("Downloaded content is not an image")
            print("Downloaded content is not an image")
            return

        # ارسال تصویر به کانال اصلی
        with open(filename, "rb") as f:
            response = requests.post(bot_url + 'sendPhoto', data={'chat_id': chat_id}, files={'photo': f})

        if response.status_code == 200:
            print('Image sent successfully!')
            log('Image sent successfully!')
        else:
            print('Error in sending image:', response.status_code)
            log(f'Error in sending image: {response.status_code}')

        # ارسال همان عکس به عنوان فایل با کیفیت بالا
        with open(filename, "rb") as f:
            response = requests.post(bot_url + 'sendDocument', data={'chat_id': chat_id}, files={'document': f})

        if response.status_code == 200:
            print('Document sent successfully!')
            log('Document sent successfully!')
        else:
            print('Error in sending document:', response.status_code)
            log(f'Error in sending document: {response.status_code}')

    except Exception as e:
        print("An error occurred:", str(e))
        log(f"An error occurred: {str(e)}")

def log(message):
    try:
        log_resp = requests.post(bot_url + "sendMessage", data={"chat_id": log_channel_id, "text": message})
        if log_resp.status_code == 200:
            print('Log registered')
        else:
            print('Error in registering log:', log_resp.status_code)
    except Exception as e:
        print("Logging failed:", str(e))

if __name__ == "__main__":
    main()
