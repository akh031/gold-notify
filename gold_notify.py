import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1513943006850584778/tkEqkwq2xDz7dz-VkIjue4M6WFdT99UG3RLLasGcVwX6jsJUbr5veQuUSJPpV0TTtcFG"

def get_gold_price():
    headers = {"User-Agent": "Mozilla/5.0"}

    r1 = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d&range=1d", headers=headers, timeout=10)
    xau_usd = r1.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]

    r2 = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/USDTHB=X?interval=1d&range=1d", headers=headers, timeout=10)
    usd_thb = r2.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]

    oz_thb = xau_usd * usd_thb                        # 99.99% ต่อออนซ์ (THB)
    baht_9999 = oz_thb / 32.1507 * 15.244             # 99.99% ต่อบาททอง (THB)
    baht_9999_usd = baht_9999 / usd_thb               # 99.99% ต่อบาททอง (USD)
    baht_965 = baht_9999 * 0.965                      # 96.5% ต่อบาททอง (THB)

    return round(xau_usd, 2), round(usd_thb, 2), round(oz_thb, 2), round(baht_9999, 2), round(baht_9999_usd, 2), round(baht_965, 2)

def send_discord(xau_usd, usd_thb, oz_thb, baht_9999, baht_9999_usd, baht_965):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    message = (
        f"🥇 **ราคาทองคำวันนี้** ({now})\n\n"
        f"💱 USD/THB: `{usd_thb:,.2f}` บาท\n\n"
        f"🔶 **ทอง 99.99%**\n"
        f"  • ต่อออนซ์: `{xau_usd:,.2f}` USD  |  `{oz_thb:,.2f}` บาท\n"
        f"  • ต่อบาททอง: `{baht_9999_usd:,.2f}` USD  |  `{baht_9999:,.2f}` บาท\n\n"
        f"🔸 **ทอง 96.5%**\n"
        f"  • ต่อบาททอง: `{baht_965:,.2f}` บาท\n\n"
        f"📊 ข้อมูลจาก Yahoo Finance"
    )
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    print("✅ ส่งสำเร็จ")

if __name__ == "__main__":
    xau_usd, usd_thb, oz_thb, baht_9999, baht_9999_usd, baht_965 = get_gold_price()
    send_discord(xau_usd, usd_thb, oz_thb, baht_9999, baht_9999_usd, baht_965)
