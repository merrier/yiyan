import time
from src.config import TARGET_URL, DATA_FILE
from src.scraper import fetch_page
from src.parser import parse_data
from src.storage import save_to_json

def main():
    print(f"开始抓取数据: {TARGET_URL}")
    
    # 1. 获取网页/API内容
    content = fetch_page(TARGET_URL)
    
    if content:
        # 2. 解析数据 (is_json=True表示目标是返回JSON的API)
        # 如果你爬取的是网页，请将其改为 False，并在 parser.py 中实现 BeautifulSoup 逻辑
        quote_data = parse_data(content, is_json=True)
        
        if quote_data:
            print(f"抓取成功: 「{quote_data['text']}」 —— {quote_data['author']}《{quote_data['source']}》")
            # 3. 保存数据到 JSON 文件
            save_to_json(quote_data, DATA_FILE)
        else:
            print("未能提取到有效数据")
    else:
        print("抓取失败")

if __name__ == "__main__":
    # 示例运行一次，如果需要持续爬取，可加上 while 循环和 time.sleep
    main()
