import json
# 如果后续需要解析网页，取消下面这行的注释
# from bs4 import BeautifulSoup

def parse_data(content, is_json=True):
    """
    解析抓取到的内容。
    如果是JSON API，直接提取对应字段；
    如果是HTML，可以使用BeautifulSoup提取DOM节点中的文本。
    """
    if not content:
        return None
        
    if is_json:
        try:
            data = json.loads(content)
            # 以一言API(hitokoto.cn)返回的格式为例
            # 根据你实际爬取的网站，请修改这里的字段名称
            return {
                "text": data.get("hitokoto", ""),
                "author": data.get("from_who", "佚名") or "佚名",
                "source": data.get("from", "未知")
            }
        except json.JSONDecodeError:
            print("解析JSON失败")
            return None
    else:
        # TODO: 解析HTML示例
        # soup = BeautifulSoup(content, 'html.parser')
        # text = soup.find('div', class_='quote-text').text.strip()
        # author = soup.find('span', class_='author').text.strip()
        # return {"text": text, "author": author, "source": ""}
        pass
        
    return None
