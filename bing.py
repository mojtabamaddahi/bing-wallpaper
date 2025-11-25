import requests
import random
from variables import bot_url, chat_id, log_channel_id

API_KEY = "53401345-ddeb36315024ea5eca9cf9cf3"
TOPIC = "nature"
PER_PAGE = 10  # تعداد عکس‌هایی که می‌خوایم انتخاب رندوم کنیم
FILENAME = "wallpaper.jpg"

def main():
    try:
        # گرفتن عکس‌ها از Pixabay
        url = f"https://pixabay.com/api/?key={API_KEY}&q={TOPIC}&image_type=photo&orientation=horizontal&per_page={PER_PAGE}"
        response = requests.get(url).json()
        images = response.get('hits', [])
        if not images:
            log("No images returned from Pixabay")
            print("No images returned from Pixabay")
            return

        # انتخاب رندوم یک عکس
        image_url = random.choice(images)['largeImageURL']
        r = requests.get(image_url)
        with open(FILENAME, "wb") as f:
            f.write(r.content)
        print("Image downloaded:", image_url)

        # ارسال عکس به کانال تلگرام
        with open(FILENAME, "rb") as f:
            resp = requests.post(bot_url + 'sendPhoto', data={'chat_id': chat_id}, files={'photo': f})
        if resp.status_code == 200:
            log("Image sent successfully!")
        else:
            log(f"Error sending image: {resp.status_code}")

    except Exception as e:
        log(f"An error occurred: {str(e)}")
        print("Error:", str(e))

def log(message):
    try:
        requests.post(bot_url + "sendMessage", data={"chat_id": log_channel_id, "text": message})
        print("Log:", message)
    except:
        print("Failed to send log:", message)

if __name__ == "__main__":
    main()
