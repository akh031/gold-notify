import requests
from bs4 import BeautifulSoup
from datetime import datetime

https://discordapp.com/api/webhooks/1513943006850584778/tkEqkwq2xDz7dz-VkIjue4M6WFdT99UG3RLLasGcVwX6jsJUbr5veQuUSJPpV0TTtcFG
def get_gold_price():
    url = "https://www.goldtraders.or.th/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    # ราคาทองสมาคมค้าทองคำ
    rows = soup.select("table.table-gold tr")
    data = {}
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            label = cols[0].get_text(strip=True)
            buy   = cols[1].get_text(strip=True)
            sell  = cols[2].get_text(strip=True)
            if "96.5" in label or "99.99" in label or "สร้อย" in label:
                data[label] = {"buy": buy, "sell": sell}
    return data

def send_discord(data):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    lines = [f"🥇 **ราคาทองคำวันนี้** ({now})\n"]
    for name, price in data.items():
        lines.append(f"**{name}**")
        lines.append(f"  รับซื้อ: `{price['buy']}` บาท")
        lines.append(f"  ขายออก: `{price['sell']}` บาท\n")
    
    lines.append("📊 ข้อมูลจาก: สมาคมค้าทองคำ (goldtraders.or.th)")
    message = "\n".join(lines)

    payload = {"content": message}
    res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if res.status_code in (200, 204):
        print("✅ ส่งสำเร็จ")
    else:
        print(f"❌ ส่งไม่สำเร็จ: {res.status_code} {res.text}")

if __name__ == "__main__":
    data = get_gold_price()
    if data:
        send_discord(data)
    else:
        print("❌ ดึงราคาทองไม่ได้")
