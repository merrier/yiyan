# 爬虫配置文件

# 目标网站URL（此处以一言API为例，后续可替换为你需要爬取的真实网页或API）
TARGET_URL = "https://v1.hitokoto.cn/"

# 请求头，伪装成浏览器防止被反爬
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 数据保存路径
DATA_FILE = "data/quotes.json"
