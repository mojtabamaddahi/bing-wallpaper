import requests, os
from variables import peapix_url, bot_url, chat_id, log_channel_id

def main():
    os.chdir(os.path.realpath(os.path.dirname(__file__)))  # تغییر مسیر به مسیر فایل
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    response = requests.get(peapix_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        date = data[0]["date"]
        imageUrl = data[0]["imageUrl"]
        print(date)
        print(imageUrl)
        if date_exists(date):
            print(f"date {date} already exists")
            log(f"date {date} already exists")
        else:
            os.makedirs("./dates", exist_ok=True)
            with open(f"./dates/{date}", 'w') as file:
                file.write(imageUrl)
            send_to_channel(date)
    else:
        print('Error:', response.status_code)
        log(f'Error: {response.status_code}')

def date_exists(date):
    return os.path.isfile(f"./dates/{date}")

def send_to_channel(date):
    with open(f"./dates/{date}", 'r') as file:
        imageUrl = file.read()

    # ارسال عکس
    response = requests.post(bot_url + 'sendPhoto', data={
        'chat_id': chat_id,
        'photo': imageUrl,
        'caption': f"bing wallpaper of {date}\n\n{chat_id}"
    })
    if response.status_code == 200:
        print(f'Image of {date} sent successfully!')
        log(f'Image of {date} sent successfully!')
    else:
        print('Error in sending image of', date, ':', response.status_code)
        log(f'Error in sending image of {date} : {response.status_code}')

    # ارسال فایل با کیفیت بالا
    response = requests.post(bot_url + 'sendDocument', data={
        'chat_id': chat_id,
        'document': imageUrl,
        'caption': f"high quality bing wallpaper of {date}\n\n{chat_id}"
    })
    if response.status_code == 200:
        print(f'document of {date} sent successfully!')
        log(f'document of {date} sent successfully!')
    else:
        print('Error in sending document of', date, ':', response.status_code)
        log(f'Error in sending document of {date} : {response.status_code}')

def log(log_message):
    log_resp = requests.post(bot_url + "sendMessage", data={
        "chat_id": log_channel_id,
        "text": log_message
    })
    if log_resp.status_code == 200:
        print('log registered')
    else:
        print('Error in registering log:', log_resp.status_code)

if __name__ == "__main__":
    main()
