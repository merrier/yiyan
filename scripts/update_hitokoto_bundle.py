import urllib.request
import json
import os
import sys
import argparse

GITHUB_REPO = "hitokoto-osc/sentences-bundle"
DATA_DIR = "data"
VERSION_FILE = os.path.join(DATA_DIR, "hitokoto_version.txt")

# 根据 https://developer.hitokoto.cn/sentence/ 映射关系
TYPE_MAP = {
    'a': '动画',
    'b': '漫画',
    'c': '游戏',
    'd': '文学',
    'e': '原创',
    'f': '来自网络',
    'g': '其他',
    'h': '影视',
    'i': '诗词',
    'j': '网易云',
    'k': '哲学',
    'l': '抖机灵'
}

def get_latest_version():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/tags"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
        
    try:
        with urllib.request.urlopen(req) as response:
            tags = json.loads(response.read().decode('utf-8'))
            if not tags:
                return None
            latest_tag = tags[0]['name']
            return latest_tag[1:] if latest_tag.startswith('v') else latest_tag
    except Exception as e:
        print(f"Failed to fetch tags: {e}")
        return None

def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def update_data(version):
    print(f"Updating data to version {version}...")
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/sentences?ref=v{version}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
        
    try:
        with urllib.request.urlopen(req) as response:
            files = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Failed to fetch file list: {e}")
        return False
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 按照类型存储数据的字典
    typed_data = {type_key: [] for type_key in TYPE_MAP.keys()}
    total_sentences = 0
    
    for f in files:
        file_name = f.get('name', '')
        if file_name.endswith('.json'):
            # 假设文件名是 a.json, b.json 等
            type_key = file_name.split('.')[0]
            
            # 如果存在不在映射表里的新类型，也动态加进去作为 "未知类型"
            if type_key not in typed_data:
                typed_data[type_key] = []
                TYPE_MAP[type_key] = f'未知类型_{type_key}'
            
            download_url = f"https://cdn.jsdelivr.net/gh/{GITHUB_REPO}@{version}/sentences/{file_name}"
            print(f"Downloading {file_name} from {download_url}...")
            
            try:
                dl_req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(dl_req) as dl_response:
                    content = dl_response.read().decode('utf-8')
                    data = json.loads(content)
                    typed_data[type_key].extend(data)
                    total_sentences += len(data)
            except Exception as e:
                print(f"Failed to download {file_name}: {e}")
                
    if total_sentences == 0:
        print("No data was downloaded.")
        return False
        
    # 分别保存为单独的 json 文件
    for type_key, sentences in typed_data.items():
        if not sentences:
            continue
            
        type_name = TYPE_MAP.get(type_key, type_key)
        # 文件命名格式： a_动画.json
        output_file = os.path.join(DATA_DIR, f"{type_key}_{type_name}.json")
        
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(sentences, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(sentences)} sentences to {output_file}")
        
    # 更新版本号
    with open(VERSION_FILE, "w", encoding='utf-8') as f:
        f.write(version)
        
    print(f"Successfully updated to v{version}. Total sentences: {total_sentences}")
    
    # Export version to GitHub Actions environment variable if possible
    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        with open(github_env, "a") as f:
            f.write(f"NEW_VERSION={version}\n")
            
    return True

def main():
    parser = argparse.ArgumentParser(description="Update Hitokoto Bundle Data")
    parser.add_argument("--force", action="store_true", help="Force update even if version is up-to-date")
    args = parser.parse_args()

    latest = get_latest_version()
    if not latest:
        print("Could not determine the latest version.")
        sys.exit(1)
        
    current = get_current_version()
    print(f"Latest version: {latest}")
    print(f"Current version: {current}")
    
    if args.force or latest != current:
        success = update_data(latest)
        if not success:
            sys.exit(1)
    else:
        print("Already up-to-date. Use --force to update anyway.")

if __name__ == "__main__":
    main()
