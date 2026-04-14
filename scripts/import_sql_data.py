import urllib.request
import re
import json
import os

def fetch_and_parse_sql():
    url = "https://raw.githubusercontent.com/abinnz/yiyan/master/yiyan-etc/sql/yiyan_data.sql"
    print(f"Downloading from {url}...")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to download: {e}")
        return

    # 解析 SQL 语句提取句子
    # 格式类似: INSERT INTO `chicken_soup` VALUES (1, 0, '句子内容', '2019...', ...);
    # 或者可能有别的表？
    
    # 我们用一个稍微通用的正则提取 VALUES 里面的第三个参数内容
    # 假设结构是: INSERT INTO `table_name` VALUES (id, type_id, 'sentence', ...);
    
    # 匹配 INSERT INTO `xxx` VALUES (xxx, xxx, '内容', ...
    # 考虑到句子中可能包含转义单引号 \'
    pattern = re.compile(r"INSERT INTO `[^`]+` VALUES \(\d+,\s*\d+,\s*'(.*?)',\s*'")
    
    sentences = []
    for line in content.splitlines():
        if line.startswith('INSERT INTO'):
            match = pattern.search(line)
            if match:
                sentence = match.group(1)
                # 处理可能存在的转义单引号
                sentence = sentence.replace("\\'", "'").replace('\\"', '"')
                sentences.append({
                    "text": sentence,
                    "author": "佚名",
                    "source": "yiyan_data.sql"
                })
                
    print(f"Successfully extracted {len(sentences)} sentences.")
    
    # 保存到 data 文件夹
    output_filename = "data/yiyan_github_dataset.json"
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(sentences, f, ensure_ascii=False, indent=4)
        
    print(f"Data successfully saved to {output_filename}")

if __name__ == "__main__":
    fetch_and_parse_sql()
