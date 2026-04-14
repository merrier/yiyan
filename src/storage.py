import json
import os

def save_to_json(data, filename):
    """
    将字典数据保存到JSON文件中。
    如果文件已存在，则追加到现有的JSON数组中。
    """
    # 确保目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    existing_data = []
    
    # 读取已有的数据
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            # 如果文件为空或格式错误，重新开始
            existing_data = []
            
    # 追加新数据
    existing_data.append(data)
    
    # 写回文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
    
    print(f"数据已成功保存至 {filename}")
