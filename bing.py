import requests
import random
from variables import bot_url, chat_id, log_channel_id

API_KEY = "53401345-ddeb36315024ea5eca9cf9cf3"  # API توی Pixabay
SEARCH_QUERY = "nature+snow+hill"
PER_PAGE = 20
FILENAME = "wallpaper.jpg"

def main():
    try:
        # گرفتن عکس‌های با کیفیت
        url = f"https://pixabay.com/api/?key={API_KEY}&q={SEARCH_QUERY}&image_type=photo&orientation=horizontal&per_page={PER_PAGE}"
        resp = requests.get(url)
        data = resp.json()
        hits = data.get("hits", [])
        if not hits:
            log("No images found for query: " + SEARCH_QUERY)
            print("No images found")
            return

        # انتخاب رندوم عکس با کیفیت
        image_url = random.choice(hits)["largeImageURL"]
        r2 = requests.get(image_url)
        with open(FILENAME, "wb") as f:
            f.write(r2.content)
        print("High-quality image downloaded:", image_url)

        # ارسال عکس به کانال تلگرام
        with open(FILENAME, "rb") as f:
            resp2 = requests.post(bot_url + "sendPhoto", data={"chat_id": chat_id}, files={"photo": f})

        if resp2.status_code == 200:
            log("High-quality image sent successfully")
        else:
            log("Error sending image: " + str(resp2.status_code))
            print("Error sending image:", resp2.status_code)

    except Exception as e:
        log("Error in main: " + str(e))
        print("Exception:", str(e))

def log(msg):
    try:
        requests.post(bot_url + "sendMessage", data={"chat_id": log_channel_id, "text": msg})
        print("Log:", msg)
    except Exception as e:
        print("Failed log:", str(e))

if __name__ == "__main__":
    main()
