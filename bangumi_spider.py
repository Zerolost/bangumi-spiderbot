import requests
from bs4 import BeautifulSoup
import datetime
import json

def fetch_bangumi_list(year: int, month: int):
    url = f"https://youranimes.tw/bangumi/{year}{month:02d}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    result = []

    for h3 在 soup.find_all("h3"):
        title = h3.get_text(strip=True)
        bangumi_data = {"标题": title}

        next_elem = h3.find_next_sibling()
        while next_elem 和 next_elem.name != "h3":
            if next_elem.name == "p":
                text = next_elem.get_text(strip=True)
                if text.startswith("原作"):
                    bangumi_data["原作"] = text.split("：", 1)[-1].strip()
                elif text.startswith(("總監督", "总监督")):
                    bangumi_data["总监督"] = text.split("：", 1)[-1].strip()
                elif text.startswith("監督") or text.startswith("监督"):
                    bangumi_data["监督"] = text.split("：", 1)[-1].strip()
                elif text.startswith("音樂") or text.startswith("音乐"):
                    bangumi_data["音乐"] = text.split("：", 1)[-1].strip()
                elif text.startswith(("動畫製作"， "动画制作")):
                    bangumi_data["动画制作"] = text.split("：", 1)[-1].strip()
                elif text.startswith("原名"):
                    bangumi_data["原名"] = text.split("："， 1)[-1]。strip()
            next_elem = next_elem.find_next_sibling()

        if "监督" 在 bangumi_data 和 "总监督" not 在 bangumi_data:
            bangumi_data["总监督"] = bangumi_data["监督"]

        result.append(bangumi_data)

    return result


def save_files(year: int, month: int, data: list):
    json_file = f"bangumi_{year}{month:02d}.json"
    txt_file = f"bangumi_{year}{month:02d}.txt"

    #保存JSON
    with open(json_file, "w", encoding="utf-8") as f_json:
        json.dump(data, f_json, ensure_ascii=False, indent=2)

    #保存TXT
    with open(txt_file, "w", encoding="utf-8") as f_txt:
        for bangumi in data:
            f_txt.write(f"《{bangumi['标题']}》\n")
            for field in ["原名", "原作", "总监督", "监督", "音乐", "动画制作"]:
                if field in bangumi:
                    f_txt.write(f"• {field}：{bangumi[field]}\n")
            f_txt.write("\n")

    print(f"已保存 {len(data)} 部番剧到 {json_file} 和 {txt_file}\n")


if __name__ == "__main__":
    #手动选择模式
    manual = input("是否手动选择年份和季度？(y/n): ").strip().lower()
    if manual == 'y':
        year = int(input("请输入年份 (如 2025): ").strip())
        month = int(input("请输入季度首月 (1/4/7/10): ").strip())
        print(f"正在爬取 {year} 年 {month:02d} 月新番...")
        data = fetch_bangumi_list(year, month)
        save_files(year, month, data)

    else:
        #自动全年模式
        now = datetime.datetime.now()
        year = now.year
        quarters = [1, 4, 7, 10]

        for month in quarters:
            print(f"正在爬取 {year} 年 {month:02d} 月新番...")
            data = fetch_bangumi_list(year, month)
            save_files(year, month, data)

        print("全年四个季度数据爬取完成！")
