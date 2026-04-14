import requests
from src.config import HEADERS

def fetch_page(url):
    """
    发送HTTP请求，获取网页HTML或API返回的JSON内容。
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        # 检查响应状态码是否为200
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None
