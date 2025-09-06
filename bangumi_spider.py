import requests
from bs4 import BeautifulSoup
import json
import datetime

def fetch_bangumi_list(year: int, month: int):
    url = f"https://youranimes.tw/bangumi/{year}{month:02d}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"请求失败: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    bangumi_list = []

    #选择器根据页面结构修改
    items = soup.select(".bangumi-item")
    for item in items:
        title = item.select_one(".bangumi-title")
        cover = item.select_one("img")
        link = item.select_one("a")

        bangumi_list.append({
            "title": title.get_text(strip=True) if title else "未知标题",
            "cover": cover["src"] if cover else None,
            "link": link["href"] if link else None
        })

    return bangumi_list


if __name__ == "__main__":
    now = datetime.datetime.now()
    month = (now.month - 1) // 3 * 3 + 1
    if month <= 3: month = 1
    elif month <= 6: month = 4
    elif month <= 9: month = 7
    else: month = 10

    result = fetch_bangumi_list(now.year, month)

    with open("bangumi.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"已保存 {len(result)} 部番剧到 bangumi.json")
