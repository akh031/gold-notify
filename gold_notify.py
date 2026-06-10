import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1513943006850584778/tkEqkwq2xDz7dz-VkIjue4M6WFdT99UG3RLLasGcVwX6jsJUbr5veQuUSJPpV0TTtcFG"

def get_gold_price():
    # ดึงราคาทองเป็น USD/oz แล้วแปลงเป็นบาท
    url = "https://data-asg.goldprice.org/dbXRates/USD"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    data = res.json()
    usd_per_oz = data["items"][0]["xauPrice"]
    usd_thb = data["items"][0]["usdPrice"]
    thb_per_oz = usd_per_oz * usd_thb
    thb_per_baht_weight = thb_per_oz / 32.1507 * 15.244  # แปลงเป็นบาททอง
    return round(thb_per_oz, 2), round(thb_per_baht_weight, 2)

def send_discord(oz, baht_weight):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    message = (
        f"🥇 **ราคาทองคำวนนี้** ({now})\n"
        f"💰 ราคา/ออนซ์: `{oz:,.2f}` บาท\n"
        f"💰 ราคา/บาททอง: `{baht_weight:,.2f}` บาท\n"
        f"📊 ข้อมูลจาก GoldPrice.org"
    )
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    print("✅ ส่งสำเร็จ")

if __name__ == "__main__":
    oz, baht_weight = get_gold_price()
    send_discord(oz, baht_weight)
