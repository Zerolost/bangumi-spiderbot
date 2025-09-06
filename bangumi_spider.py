import requests
from bs4 import BeautifulSoup
import json
import datetime

def fetch_bangumi_list(year: int, month: int):
    url = f"https://youranimes.tw/bangumi/{year}{month:02d}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    result = []
    for h3 in soup.find_all("h3"):
        title = h3.get_text(strip=True)

        next_elem = h3.find_next_sibling()
        info = {}
        while next_elem and next_elem.name != "h3":
            text = next_elem.get_text(strip=True)
            if "首播" in text:
                info["broadcast"] = text
            next_elem = next_elem.find_next_sibling()

        result.append({
            "title": title,
            **info
        })
    return result

if __name__ == "__main__":
    now = datetime.datetime.now()
    month = (now.month - 1) // 3 * 3 + 1
    month = month if month in (1,4,7,10) else (1 if month <= 3 else 4 if month <= 6 else 7 if month <= 9 else 10)

    data = fetch_bangumi_list(now.year, month)
    with open("bangumi.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已保存 {len(data)} 部番剧信息到 bangumi.json")
