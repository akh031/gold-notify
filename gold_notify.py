import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1513943006850584778/tkEqkwq2xDz7dz-VkIjue4M6WFdT99UG3RLLasGcVwX6jsJUbr5veQuUSJPpV0TTtcFG"

def get_gold_price():
    # ราคาทองจาก Yahoo Finance API (เปิดแนนอน)
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    r1 = requests.get(url, headers=headers, timeout=10)
    data = r1.json()
    xau_usd = data["chart"]["result"][0]["meta"]["regularMarketPrice"]

    # อัตราแลกเปลี่ยน USD/THB
    url2 = "https://query1.finance.yahoo.com/v8/finance/chart/USDTHB=X?interval=1d&range=1d"
    r2 = requests.get(url2, headers=headers, timeout=10)
    data2 = r2.json()
    usd_thb = data2["chart"]["result"][0]["meta"]["regularMarketPrice"]

    thb_per_oz = xau_usd * usd_thb
    thb_per_baht = thb_per_oz / 32.1507 * 15.244
    return round(xau_usd, 2), round(usd_thb, 2), round(thb_per_oz, 2), round(thb_per_baht, 2)

def send_discord(xau_usd, usd_thb, thb_oz, thb_baht):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    message = (
        f"🥇 **ราคาทองคำวนนี้** ({now})\n"
        f"🌍 ทองโลก: `{xau_usd:,.2f}` USD/oz\n"
        f"💱 อัตราแลกเปลี่ยน: `{usd_thb:,.2f}` บาท/USD\n"
        f"💰 ราคา/ออนซ์: `{thb_oz:,.2f}` บาท\n"
        f"💰 ราคา/บาททอง (ประมาณ): `{thb_baht:,.2f}` บาท\n"
        f"📊 ข้อมูลจาก Yahoo Finance"
    )
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    print("✅ ส่งสำเร็จ")

if __name__ == "__main__":
    xau_usd, usd_thb, thb_oz, thb_baht = get_gold_price()
    send_discord(xau_usd, usd_thb, thb_oz, thb_baht)
