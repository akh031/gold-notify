import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1513943006850584778/tkEqkwq2xDz7dz-VkIjue4M6WFdT99UG3RLLasGcVwX6jsJUbr5veQuUSJPpV0TTtcFG"

def get_gold_price():
    headers = {"User-Agent": "Mozilla/5.0"}

    # ราคาทองโลก USD/oz
    r1 = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d&range=1d", headers=headers, timeout=10)
    xau_usd = r1.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]

    # อัตราแลกเปลี่ยน
    r2 = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/USDTHB=X?interval=1d&range=1d", headers=headers, timeout=10)
    usd_thb = r2.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]

    thb_per_oz = xau_usd * usd_thb
    gold_9999 = thb_per_oz / 32.1507 * 15.244        # ทอง 99.99%
    gold_965 = gold_9999 * 0.965                      # ทอง 96.5%

    return round(xau_usd, 2), round(usd_thb, 2), round(gold_9999, 2), round(gold_965, 2)

def send_discord(xau_usd, usd_thb, gold_9999, gold_965):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    message = (
        f"🥇 **ราคาทองคำวันนี้** ({now})\n\n"
        f"🌍 ทองโลก: `{xau_usd:,.2f}` USD/oz\n"
        f"💱 USD/THB: `{usd_thb:,.2f}` บาท\n\n"
        f"🔶 ทอง 99.99%: `{gold_9999:,.2f}` บาท/บาททอง\n"
        f"🔸 ทอง 96.5%: `{gold_965:,.2f}` บาท/บาททอง\n\n"
        f"📊 ข้อมูลจาก Yahoo Finance"
    )
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    print("✅ ส่งสำเร็จ")

if __name__ == "__main__":
    xau_usd, usd_thb, gold_9999, gold_965 = get_gold_price()
    send_discord(xau_usd, usd_thb, gold_9999, gold_965)
