import requests
from bs4 import BeautifulSoup
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1513943006850584778/tkEqkwq2xDz7dz-VkIjue4M6WFdT99UG3RLLasGcVwX6jsJUbr5veQuUSJPpV0TTtcFG"

def get_gold_price():
    url = "https://chaiseri.co.th/gold/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    prices = soup.select(".price-value")
    result = {}
    if len(prices) >= 2:
        result["ทองคำแท่ง รับซื้อ"] = prices[0].get_text(strip=True)
        result["ทองคำแท่ง ขายออก"] = prices[1].get_text(strip=True)
    return result

def send_discord(data):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    lines = [f"🥇 **ราคาทองคำไทยวันนี้** ({now})\n"]
    for k, v in data.items():
        lines.append(f"**{k}:** `{v}` บาท")
    lines.append("\n📊 ข้อมูลจาก: ไชยเศรษฐ์")
    message = "\n".join(lines)
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    print("✅ ส่งสำเร็จ")

if __name__ == "__main__":
    data = get_gold_price()
    if data:
        send_discord(data)
    else:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": "⚠️ ดึงราคาทองไม่ได้ กรุณาตรวจสอบ"})
