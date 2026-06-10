import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1513943006850584778/tkEqkwq2xDz7dz-VkIjue4M6WFdT99UG3RLLasGcVwX6jsJUbr5veQuUSJPpV0TTtcFG"

def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/THB"
    headers = {"x-access-token": "goldapi-free"}
    res = requests.get(url, headers=headers, timeout=10)
    data = res.json()
    price = data.get("price", 0)
    return float(price)

def send_discord(price):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    message = f"🥇 **ราคาทองคำวันนี้** ({now})\n💰 ราคา: `{price:,.2f}` บาท/ออนซ์\n📊 ข้อมูลจาก GoldAPI"
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    print("✅ ส่งสำเร็จ")

if __name__ == "__main__":
    price = get_gold_price()
    send_discord(price)
