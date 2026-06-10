import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1513943006850584778/tkEqkwq2xDz7dz-VkIjue4M6WFdT99UG3RLLasGcVwX6jsJUbr5veQuUSJPpV0TTtcFG"

def get_gold_price():
    # ใช้ frankfurter API ดึง USD/THB แล้วคำนวณราคาทอง
    # ราคาทองโลก USD/oz จาก metals.live (ฟรี ไม่บล็อก)
    r1 = requests.get("https://metals.live/api/v1/spot", timeout=10)
    metals = r1.json()
    xau_usd = None
    for item in metals:
        if "gold" in item:
            xau_usd = float(item["gold"])
            break

    # อัตราแลกเปลี่ยน USD/THB
    r2 = requests.get("https://api.frankfurter.app/latest?from=USD&to=THB", timeout=10)
    fx = r2.json()
    usd_thb = fx["rates"]["THB"]

    thb_per_oz = xau_usd * usd_thb
    thb_per_baht = thb_per_oz / 32.1507 * 15.244
    return round(xau_usd, 2), round(thb_per_oz, 2), round(thb_per_baht, 2)

def send_discord(xau_usd, thb_oz, thb_baht):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    message = (
        f"🥇 **ราคาทองคำวันนี้** ({now})\n"
        f"🌍 ราคาโลก: `{xau_usd:,.2f}` USD/oz\n"
        f"💰 ราคา/ออนซ์: `{thb_oz:,.2f}` บาท\n"
        f"💰 ราคา/บาททอง (ประมาณ): `{thb_baht:,.2f}` บาท\n"
        f"📊 ข้อมูลจาก metals.live + frankfurter"
    )
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    print("✅ ส่งสำเร็จ")

if __name__ == "__main__":
    xau_usd, thb_oz, thb_baht = get_gold_price()
    send_discord(xau_usd, thb_oz, thb_baht)
